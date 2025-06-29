#███╗   ██╗ ██████╗ ████████╗██████╗ ██╗████████╗██╗██╗  ██╗
#████╗  ██║██╔═══██╗╚══██╔══╝██╔══██╗██║╚══██╔══╝██║██║ ██╔╝
#██╔██╗ ██║██║   ██║   ██║   ██████╔╝██║   ██║   ██║█████╔╝ 
#██║╚██╗██║██║   ██║   ██║   ██╔══██╗██║   ██║   ██║██╔═██╗ 
#██║ ╚████║╚██████╔╝   ██║   ██║  ██║██║   ██║   ██║██║  ██╗
#╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝╚═╝  ╚═╝
                                                           


import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from typing import Dict, Optional
import json

# Bot configuration
EMBED_COLOR = discord.Color.blurple()
DEFAULT_BITRATE = 64000
DEFAULT_USER_LIMIT = 0

# Initialize bot with required intents
intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Store temporary voice channel data
temp_vc_data: Dict[int, dict] = {}

# Custom View for VC Control Panel
class VCControlPanel(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🔒 Lock", style=discord.ButtonStyle.grey, custom_id="vc_lock")
    async def lock_vc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_ownership(interaction):
            return
        
        channel_id = temp_vc_data.get(interaction.user.id, {}).get("channel_id")
        if not channel_id:
            return await interaction.response.send_message("You don't own a voice channel!", ephemeral=True)
        
        channel = interaction.guild.get_channel(channel_id)
        await channel.set_permissions(interaction.guild.default_role, connect=False)
        await interaction.response.send_message("Voice channel locked! 🔒", ephemeral=True)

    @discord.ui.button(label="🔓 Unlock", style=discord.ButtonStyle.grey, custom_id="vc_unlock")
    async def unlock_vc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_ownership(interaction):
            return
        
        channel_id = temp_vc_data.get(interaction.user.id, {}).get("channel_id")
        if not channel_id:
            return await interaction.response.send_message("You don't own a voice channel!", ephemeral=True)
        
        channel = interaction.guild.get_channel(channel_id)
        await channel.set_permissions(interaction.guild.default_role, connect=True)
        await interaction.response.send_message("Voice channel unlocked! 🔓", ephemeral=True)

    @discord.ui.button(label="👁 Hide", style=discord.ButtonStyle.grey, custom_id="vc_hide")
    async def hide_vc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_ownership(interaction):
            return
        
        channel_id = temp_vc_data.get(interaction.user.id, {}).get("channel_id")
        if not channel_id:
            return await interaction.response.send_message("You don't own a voice channel!", ephemeral=True)
        
        channel = interaction.guild.get_channel(channel_id)
        await channel.set_permissions(interaction.guild.default_role, view_channel=False)
        await interaction.response.send_message("Voice channel hidden! 👁", ephemeral=True)

    @discord.ui.button(label="👁‍🗨 Unhide", style=discord.ButtonStyle.grey, custom_id="vc_unhide")
    async def unhide_vc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_ownership(interaction):
            return
        
        channel_id = temp_vc_data.get(interaction.user.id, {}).get("channel_id")
        if not channel_id:
            return await interaction.response.send_message("You don't own a voice channel!", ephemeral=True)
        
        channel = interaction.guild.get_channel(channel_id)
        await channel.set_permissions(interaction.guild.default_role, view_channel=True)
        await interaction.response.send_message("Voice channel unhidden! 👁‍🗨", ephemeral=True)

    @discord.ui.button(label="👥 Limit", style=discord.ButtonStyle.grey, custom_id="vc_limit")
    async def limit_vc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_ownership(interaction):
            return
        
        # Create modal for user limit input
        modal = LimitModal()
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="✏️ Rename", style=discord.ButtonStyle.grey, custom_id="vc_rename")
    async def rename_vc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_ownership(interaction):
            return
        
        # Create modal for rename input
        modal = RenameModal()
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="👑 Transfer", style=discord.ButtonStyle.grey, custom_id="vc_transfer")
    async def transfer_vc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_ownership(interaction):
            return
        
        # Create modal for transfer input
        modal = TransferModal()
        await interaction.response.send_modal(modal)

    @discord.ui.button(label="🚫 Delete", style=discord.ButtonStyle.red, custom_id="vc_delete")
    async def delete_vc(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not await self.check_ownership(interaction):
            return
        
        channel_id = temp_vc_data.get(interaction.user.id, {}).get("channel_id")
        if not channel_id:
            return await interaction.response.send_message("You don't own a voice channel!", ephemeral=True)
        
        channel = interaction.guild.get_channel(channel_id)
        await channel.delete()
        del temp_vc_data[interaction.user.id]
        await interaction.response.send_message("Voice channel deleted! 🗑️", ephemeral=True)

    async def check_ownership(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id not in temp_vc_data:
            await interaction.response.send_message("You don't own a voice channel!", ephemeral=True)
            return False
        return True

class LimitModal(discord.ui.Modal, title="Set User Limit"):
    limit = discord.ui.TextInput(
        label="User Limit",
        placeholder="Enter a number (0 for unlimited)",
        required=True,
        min_length=1,
        max_length=2
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            limit = int(self.limit.value)
            if limit < 0:
                return await interaction.response.send_message("Please enter a positive number!", ephemeral=True)
            
            channel_id = temp_vc_data.get(interaction.user.id, {}).get("channel_id")
            if not channel_id:
                return await interaction.response.send_message("You don't own a voice channel!", ephemeral=True)
            
            channel = interaction.guild.get_channel(channel_id)
            await channel.edit(user_limit=limit)
            await interaction.response.send_message(f"User limit set to {limit}! 👥", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Please enter a valid number!", ephemeral=True)

class RenameModal(discord.ui.Modal, title="Rename Voice Channel"):
    name = discord.ui.TextInput(
        label="New Name",
        placeholder="Enter new channel name",
        required=True,
        min_length=1,
        max_length=100
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel_id = temp_vc_data.get(interaction.user.id, {}).get("channel_id")
        if not channel_id:
            return await interaction.response.send_message("You don't own a voice channel!", ephemeral=True)
        
        channel = interaction.guild.get_channel(channel_id)
        await channel.edit(name=self.name.value)
        await interaction.response.send_message(f"Channel renamed to {self.name.value}! ✏️", ephemeral=True)

class TransferModal(discord.ui.Modal, title="Transfer Ownership"):
    user_id = discord.ui.TextInput(
        label="User ID",
        placeholder="Enter the user ID to transfer ownership to",
        required=True,
        min_length=17,
        max_length=20
    )

    async def on_submit(self, interaction: discord.Interaction):
        try:
            new_owner_id = int(self.user_id.value)
            member = interaction.guild.get_member(new_owner_id)
            
            if not member:
                return await interaction.response.send_message("User not found!", ephemeral=True)
            
            channel_data = temp_vc_data.pop(interaction.user.id, None)
            if not channel_data:
                return await interaction.response.send_message("You don't own a voice channel!", ephemeral=True)
            
            temp_vc_data[new_owner_id] = channel_data
            await interaction.response.send_message(f"Ownership transferred to {member.display_name}! 👑", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("Please enter a valid user ID!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.tree.command(name="setup", description="Set up Join to Create VC system")
@app_commands.describe(type="Choose setup type (jtc)")
async def setup(interaction: discord.Interaction, type: str):
    if type.lower() != "jtc":
        return await interaction.response.send_message("Invalid setup type! Use 'jtc'", ephemeral=True)

    # Create category
    category = await interaction.guild.create_category("Join to Create")
    
    # Create voice channel
    create_vc = await category.create_voice_channel("➕ Create VC")
    
    # Create interface channel
    interface = await category.create_text_channel("🍾・interface")
    
    # Create and send embed
    embed = discord.Embed(
        title="🛠️ RxLunes Interface",
        description=(
            "Use the buttons below to manage your personal voice channel.\n\n"
            "**Available Controls:**\n"
            "🔒 Lock / 🔓 Unlock - Control access to your VC\n"
            "👁 Hide / 👁‍🗨 Unhide - Control visibility of your VC\n"
            "👥 Limit - Set user limit for your VC\n"
            "✏️ Rename - Change your VC name\n"
            "👑 Transfer - Transfer ownership to another user\n"
            "🚫 Delete - Delete your temporary VC\n\n"
            "*Note: Only the VC owner can use these controls*"
        ),
        color=EMBED_COLOR
    )
    
    await interface.send(embed=embed, view=VCControlPanel())
    await interaction.response.send_message("Join to Create system has been set up! ✅", ephemeral=True)

@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    # Handle member joining Create VC
    if after.channel and after.channel.name == "➕ Create VC":
        # Create new VC
        category = after.channel.category
        new_vc = await category.create_voice_channel(
            name=f"{member.display_name}'s VC",
            bitrate=DEFAULT_BITRATE,
            user_limit=DEFAULT_USER_LIMIT
        )
        
        # Move member to new VC
        await member.move_to(new_vc)
        
        # Store VC data
        temp_vc_data[member.id] = {
            "channel_id": new_vc.id,
            "interface_id": discord.utils.get(category.text_channels, name="🍾・interface").id
        }
    
    # Handle empty temporary VC
    if before.channel and before.channel.id in [data["channel_id"] for data in temp_vc_data.values()]:
        if len(before.channel.members) == 0:
            # Find owner
            owner_id = None
            for user_id, data in temp_vc_data.items():
                if data["channel_id"] == before.channel.id:
                    owner_id = user_id
                    break
            
            if owner_id:
                del temp_vc_data[owner_id]
                await before.channel.delete()

# Run the bot
TOKEN = "YOURBOTTOKENS"  # Replace with your bot token
bot.run(TOKEN) 