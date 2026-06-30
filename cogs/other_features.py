import discord
from discord.ext import commands
import sqlite3
from .permission_handler import PermissionManager

class OtherFeatures(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def show_other_features_menu(self, interaction: discord.Interaction):
        try:
            _, is_global = PermissionManager.is_admin(interaction.user.id)

            embed = discord.Embed(
                title="🔧 Other Features",
                description=(
                    "This section was created according to users' requests:\n\n"
                    "**Available Operations**\n"
                    "━━━━━━━━━━━━━━━━━━━━━━\n"
                    "📣 **Notification System**\n"
                    "└ Event notification system\n"
                    "└ Not just for Bear! Use it for any event:\n"
                    "   Vikings - KE - Eternity's Reach and everything else\n"
                    "└ Add unlimited notifications\n\n"
                    "🆔 **ID Channel**\n"
                    "└ Create and manage ID channels\n"
                    "└ Automatic ID verification system\n"
                    "└ Custom channel settings\n\n"
                    "📝 **Registration System**\n"
                    "└ Enable/disable user self-registration (Global Admin only)\n"
                    "└ Users can /register to add themselves based on ID\n\n"
                    "📋 **Attendance System**\n"
                    "└ Manage event attendance records\n"
                    "└ View detailed attendance reports\n"
                    "└ Export attendance data to CSV, TSV, HTML\n\n"
                    "🏛️ **Minister Scheduling**\n"
                    "└ Manage your state minister appointments\n"
                    "└ Schedule Construction, Research, Training days\n"
                    "└ Configure minister log channels\n\n"
                    "💾 **Backup System**\n"
                    "└ Automatic database backup\n"
                    "└ Send backups to your DMs\n"
                    "└ Restore from backup file (/restore_backup)\n"
                    "└ Only for Global Admin\n"
                    "━━━━━━━━━━━━━━━━━━━━━━"
                ),
                color=discord.Color.blue()
            )

            view = OtherFeaturesView(self, is_global)

            try:
                await interaction.response.edit_message(embed=embed, view=view)
            except discord.InteractionResponded:
                pass

        except Exception as e:
            print(f"Error in show_other_features_menu: {e}")
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ An error occurred. Please try again.",
                    ephemeral=True
                )

class OtherFeaturesView(discord.ui.View):
    def __init__(self, cog, is_global: bool = False):
        super().__init__(timeout=None)
        self.cog = cog
        self.is_global = is_global

        # Disable global-admin-only buttons for non-global admins
        if not is_global:
            for child in self.children:
                if isinstance(child, discord.ui.Button) and child.label in [
                    "Backup System", "Registration System"
                ]:
                    child.disabled = True

    @discord.ui.button(
        label="Notification System",
        emoji="📣",
        style=discord.ButtonStyle.primary,
        custom_id="bear_trap",
        row=0
    )
    async def bear_trap_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            bear_trap_cog = self.cog.bot.get_cog("BearTrap")
            if bear_trap_cog:
                await bear_trap_cog.show_bear_trap_menu(interaction)
            else:
                await interaction.response.send_message(
                    "❌ Bear Trap module not found.",
                    ephemeral=True
                )
        except Exception as e:
            print(f"Error loading Bear Trap menu: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while loading Bear Trap menu.",
                ephemeral=True
            )

    @discord.ui.button(
        label="ID Channel",
        emoji="🆔",
        style=discord.ButtonStyle.primary,
        custom_id="id_channel",
        row=0
    )
    async def id_channel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            id_channel_cog = self.cog.bot.get_cog("IDChannel")
            if id_channel_cog:
                await id_channel_cog.show_id_channel_menu(interaction)
            else:
                await interaction.response.send_message(
                    "❌ ID Channel module not found.",
                    ephemeral=True
                )
        except Exception as e:
            print(f"Error loading ID Channel menu: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while loading ID Channel menu.",
                ephemeral=True
            )

    @discord.ui.button(
        label="Minister Scheduling",
        emoji="🏛️",
        style=discord.ButtonStyle.primary,
        custom_id="minister_channels",
        row=1
    )
    async def minister_channels_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            minister_menu_cog = self.cog.bot.get_cog("MinisterMenu")
            if minister_menu_cog:
                await minister_menu_cog.show_minister_channel_menu(interaction)
            else:
                await interaction.response.send_message(
                    "❌ Minister Scheduling module not found.",
                    ephemeral=True
                )
        except Exception as e:
            print(f"Error loading Minister Scheduling menu: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while loading Minister Scheduling menu.",
                ephemeral=True
            )

    @discord.ui.button(
        label="Backup System",
        emoji="💾",
        style=discord.ButtonStyle.primary,
        custom_id="backup_system",
        row=2
    )
    async def backup_system_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            backup_cog = self.cog.bot.get_cog("BackupOperations")
            if backup_cog:
                await backup_cog.show_backup_menu(interaction)
            else:
                await interaction.response.send_message(
                    "❌ Backup System module not found.",
                    ephemeral=True
                )
        except Exception as e:
            print(f"Error loading Backup System menu: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while loading Backup System menu.",
                ephemeral=True
            )
            
    @discord.ui.button(
        label="Registration System",
        emoji="📝",
        style=discord.ButtonStyle.primary,
        custom_id="registration_system",
        row=0
    )
    async def registration_system_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            register_cog = self.cog.bot.get_cog("Register")
            if register_cog:
                await register_cog.show_settings_menu(interaction)
            else:
                await interaction.response.send_message(
                    "❌ Registration System module not found.",
                    ephemeral=True
                )
        except Exception as e:
            print(f"Error loading Registration System menu: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while loading Registration System menu.",
                ephemeral=True
            )

    @discord.ui.button(
        label="Attendance System",
        emoji="📋",
        style=discord.ButtonStyle.primary,
        custom_id="attendance_system",
        row=1
    )
    async def attendance_system_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            attendance_cog = self.cog.bot.get_cog("Attendance")
            if attendance_cog:
                await attendance_cog.show_attendance_menu(interaction)
            else:
                await interaction.response.send_message(
                    "❌ Attendance System module not found.",
                    ephemeral=True
                )
        except Exception as e:
            print(f"Error loading Attendance System menu: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while loading Attendance System menu.",
                ephemeral=True
            )

    @discord.ui.button(
        label="Main Menu",
        emoji="🏠",
        style=discord.ButtonStyle.secondary,
        custom_id="main_menu",
        row=2
    )
    async def main_menu_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            alliance_cog = self.cog.bot.get_cog("Alliance")
            if alliance_cog:
                await alliance_cog.show_main_menu(interaction)
        except Exception as e:
            print(f"Error returning to main menu: {e}")
            await interaction.response.send_message(
                "❌ An error occurred while returning to main menu.",
                ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(OtherFeatures(bot))