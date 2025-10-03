from app.utilities import *
import sys
from rich.table import Table
from rich.console import Console
from rich.panel import Panel
import questionary
from prompt_toolkit.styles import Style
import app.db
from app.settings.host import Hosts
from app.settings.master import Master

console = Console()

hosts = Hosts()
master = Master(hosts)

db = None

def close():
    hosts.close()
    master.close()
    if db is not None:
        db.disconnect()

if not master.gethash():
    while True:
        clear()
        console.print("[bold blue]Naval Fleet Management System - Setup[/bold blue]")
        password = questionary.password("Enter new master password:").ask()
        if not password:
            console.print("[red]Password cannot be empty. Please try again.[/red]")
            sleep()
            continue
        confirm_password = questionary.password("Confirm master password:").ask()
        if password != confirm_password:
            console.print("[red]Passwords do not match. Please try again.[/red]")
            sleep()
            continue
        master.setpassword(password)
        console.print("[green]Master password set successfully.[/green]")
        sleep()
        break

while True:
    clear()
    console.print("[bold blue]Naval Fleet Management System - Login[/bold blue]")
    auth = questionary.select(
        "Select authentication method:",
        choices=[
            "Master Password",
            "Forgot Password",
            "Exit"
        ]
    ).ask()
    if auth == "Exit":
        console.print("[orange1]Exiting the system. Goodbye![/orange1]")
        close()
        sleep()
        sys.exit(0)
    elif auth == "Master Password":
        clear()
        console.print("[bold blue]Naval Fleet Management System - Login[/bold blue]")
        password = questionary.password("Enter master password:").ask()
        if not password:
            console.print("[red]Password cannot be empty. Please try again.[/red]")
            sleep()
            continue
        if not master.verifypassword(password):
            console.print("[red]Incorrect password. Please try again.[/red]")
            sleep()
            continue
        console.print("[green]Login successful.[/green]")
        sleep()
        break
    elif auth == "Forgot Password":
        clear()
        console.print("[bold blue]Naval Fleet Management System - Login[/bold blue]")
        confirm = questionary.confirm("This will delete all configured hosts and reset the master password. Are you sure?").ask()
        if not confirm:
            continue
        master.forgetpassword()
        console.print("[green]Master password reset successfully. Please set a new master password.[/green]")
        sleep()
        while True:
            clear()
            console.print("[bold blue]Naval Fleet Management System - Setup[/bold blue]")
            password = questionary.password("Enter new master password:").ask()
            if not password:
                console.print("[red]Password cannot be empty. Please try again.[/red]")
                sleep()
                continue
            confirm_password = questionary.password("Confirm master password:").ask()
            if password != confirm_password:
                console.print("[red]Passwords do not match. Please try again.[/red]")
                sleep()
                continue
            master.setpassword(password)
            console.print("[green]Master password set successfully.[/green]")
            sleep()
            break

while True:
    clear()
    console.print("[bold blue]Naval Fleet Management System[/bold blue]")
    if not hosts.gethosts():
        console.print("[yellow]No hosts configured. Please add a host to continue.[/yellow]")
        hostname = questionary.text("Enter host address (default '127.0.0.1'):", default="127.0.0.1").ask()
        if not hostname:
            console.print("[red]Host address cannot be empty. Please try again.[/red]")
            sleep(1)
            continue
        password = questionary.password("Enter host password (default 'root'):", default="root").ask()
        if not password:
            console.print("[red]Host password cannot be empty. Please try again.[/red]")
            sleep(1)
            continue
        console.print("[blue]Adding and connecting to the host...[/blue]")
        try:
            db = app.db.DB(host=hostname, password=password)
        except app.db.DatabaseConnectionError as e:
            console.print(f"Could not connect to the host.\n[red]Error: {e}[/red]")
            sleep(2)
            continue
        hosts.addhost(hostname, password)
        console.print(f"[green]Host {hostname} added successfully.[/green]")
        sleep()
        break
    else:
        hostname = questionary.select(
            "Select a host to connect:",
            choices=[host[1] for host in hosts.gethosts()] + ["Add new host", "Exit"]
        ).ask()
        if hostname == "Add new host":
            hostname = questionary.text("Enter host address (default '127.0.0.1'):", default="127.0.0.1").ask()
            password = questionary.password("Enter host password (default 'root'):", default="root").ask()
            console.print("[blue]Adding and connecting to the host...[/blue]")
            try:
                db = app.db.DB(host=hostname, password=password)
            except app.db.DatabaseConnectionError as e:
                console.print(f"Could not connect to the host.\n[red]Error: {e}[/red]")
                sleep(2)
                continue
            try:
                hosts.addhost(hostname, password)
            except Exception as e:
                console.print(f"[red]Could not add host. Error: {e}[/red]")
                sleep(2)
                continue
            console.print(f"[green]Host {hostname} added successfully.[/green]")
            sleep()
            break
        elif hostname == "Exit":
            console.print("[orange1]Exiting the system. Goodbye![/orange1]")
            close()
            sleep()
            sys.exit(0)
        else:
            password = hosts.getpassword(hostname)
            console.print("[blue]Connecting to the host...[/blue]")
            try:
                db = app.db.DB(host=hostname, password=password)
            except app.db.DatabaseConnectionError as e:
                console.print(f"Could not connect to the host.\n[red]Error: {e}[/red]")
                sleep(2)
                continue
            console.print(f"[green]Connected to host {hostname} successfully.[/green]")
            sleep()
            break

if db is not None and db.is_connected():
    while True:
        clear()
        console.print("[bold blue]Naval Fleet Management System[/bold blue]")
        custom_style = Style([
            ("cyan", "ansicyan"),
            ("blue", "ansiblue"),
            ("magenta", "ansimagenta"),
            ("yellow", "ansiyellow"),
            ("green", "ansigreen"),
            ("bright_blue", "ansibrightblue"),
            ("bold_cyan", "bold ansicyan"),
            ("bright_magenta", "ansibrightmagenta"),
            ("bright_yellow", "ansibrightyellow"),
            ("bright_cyan", "ansibrightcyan"),
            ("bright_green", "ansibrightgreen"),
            ("white", "ansiwhite"),
            ("exit", "bold ansired"),
        ])

        choices = [
            questionary.Choice(title=[("class:cyan", "1. Crews")], value="1"),
            questionary.Choice(title=[("class:blue", "2. Ships")], value="2"),
            questionary.Choice(title=[("class:magenta", "3. Missions")], value="3"),
            questionary.Choice(title=[("class:yellow", "4. Documents")], value="4"),
            questionary.Choice(title=[("class:bright_blue", "5. Inventory")], value="5"),
            questionary.Choice(title=[("class:bold_cyan", "6. Bases")], value="6"),
            questionary.Choice(title=[("class:bright_green", "7. Routes")], value="7"),
            questionary.Choice(title=[("class:bright_yellow", "8. Settings")], value="8"),
            questionary.Choice(title=[("class:exit", "Exit")], value="Exit"),
        ]

        choice = questionary.select(
            "Menu:",
            choices=choices,
            style=custom_style
        ).ask()
        
        if choice is None:
            console.print("[red]No option selected. Please try again.[/red]")
            sleep()
            continue
        elif choice == "Exit":
            console.print("[orange1]Exiting the system. Goodbye![/orange1]")
            sleep()
            break
        elif choice == "1":
            while True:
                clear()
                console.print("[bold blue]Naval Fleet Management System - Crew Management[/bold blue]")
                cchoice =  questionary.select(
                    "Crew Menu - Select an option:",
                    choices=[
                        questionary.Choice(title=[("class:blue", "Add Crew Member")], value="Add Crew Member"),
                        questionary.Choice(title=[("class:magenta", "Update Crew Member")], value="Update Crew Member"),
                        questionary.Choice(title=[("class:yellow", "Delete Crew Member")], value="Delete Crew Member"),
                        questionary.Choice(title=[("class:green", "See All Crew Members")], value="See All Crew Members"),
                        questionary.Choice(title=[("class:bright_blue", "Search Crew Member")], value="Search Crew Member"),
                        questionary.Choice(title=[("class:bright_magenta", "Crew Types")], value="Crew Types"),
                        questionary.Choice(title=[("class:bright_yellow", "Crew Status")], value="Crew Status"),
                        questionary.Choice(title=[("class:exit", "Back to Main Menu")], value="Back to Main Menu"),
                    ], style=custom_style
                ).ask()
                if cchoice == "Back to Main Menu":
                    break
                elif cchoice == "Add Crew Member":
                    clear()
                    cname = questionary.text("Enter crew member name:").ask()
                    cgender = questionary.select(
                        "Select crew member gender:",
                        choices=[
                            questionary.Choice(title="Male", value="M"),
                            questionary.Choice(title="Female", value="F"),
                            questionary.Choice(title="Other", value="O")
                        ]
                    ).ask()
                    cdob = questionary.text("Enter crew member date of birth (YYYY-MM-DD):").ask()
                    ctype = questionary.text("Enter crew member type (e.g., Officer, Sailor):").ask()
                    cstatus = questionary.select(
                        "Select crew member status:",
                        choices=["Active", "Inactive", "On Leave", "Retired"]
                    ).ask()
                    if not all([cname, cgender, cdob, ctype, cstatus]):
                        console.print("[red]All fields are required. Please try again.[/red]")
                        sleep()
                        continue
                    try:
                        db.crew.add(cname, cgender, cdob, ctype, cstatus)
                    except Exception as e:
                        console.print(f"[red]Error adding crew member: {e}[/red]")
                        sleep(1)
                        continue
                    console.print(f"[green]Crew member {cname} added successfully.[/green]")
                    sleep(2)
                elif cchoice == "Update Crew Member":
                    clear()
                    if not db.crew.fetchall():
                        console.print("[yellow]No crew members found to update.[/yellow]")
                        sleep()
                        continue
                    crew_list = db.crew.fetchall()
                    cid = questionary.text("Enter crew member ID to update:").ask()
                    if not cid or not cid.isdigit() or int(cid) < 1 or cid not in [str(crew[0]) for crew in crew_list]:
                        console.print("[red]Invalid crew member ID. Please try again.[/red]")
                        sleep()
                        continue
                    cid = int(cid)
                    cname = questionary.text("Enter new name (leave blank to keep current):").ask()
                    cgender = questionary.select(
                        "Select gender:",
                        choices=[
                            questionary.Choice(title="Male", value="M"),
                            questionary.Choice(title="Female", value="F"),
                            questionary.Choice(title="Other", value="O"),
                            "Keep current"
                        ]
                    ).ask()
                    if cgender == "Keep current":
                        cgender = None
                    cdob = questionary.text("Enter new date of birth (YYYY-MM-DD) (leave blank to keep current):").ask()
                    ctype = questionary.text("Enter new type (leave blank to keep current):").ask()
                    cstatus = questionary.select(
                        "Select status:",
                        choices=[
                            "Active",
                            "Inactive",
                            "On Leave",
                            "Retired",
                            "Keep current"
                        ]
                    ).ask()
                    if cstatus == "Keep current":
                        cstatus = None
                    if not any([cname, cgender, cdob, ctype, cstatus]):
                        console.print("[red]No updates provided. Please try again.[/red]")
                        sleep()
                        continue
                    try: 
                        db.crew.update(cid, name=cname if cname else None, gender=cgender, dob=cdob if cdob else None, crew_type=ctype if ctype else None, status=cstatus)
                    except Exception as e:
                        console.print(f"[red]Error updating crew member: {e}[/red]")
                        sleep()
                        continue
                    console.print(f"[green]Crew member ID {cid} updated successfully.[/green]")
                    sleep(2)
                elif cchoice == "Delete Crew Member":
                    clear()
                    if not db.crew.fetchall():
                        console.print("[yellow]No crew members found to delete.[/yellow]")
                        sleep()
                        continue
                    crew_list = db.crew.fetchall()
                    dopt = questionary.select(
                        "Delete Options:",
                        choices=[
                            "Delete All Crew Members",
                            "Delete Specific Crew Member",
                            "Cancel"
                        ]
                    ).ask()
                    if dopt == "Cancel":
                        console.print("[yellow]Deletion cancelled.[/yellow]")
                        sleep()
                        continue
                    elif dopt == "Delete All Crew Members":
                        confirm = questionary.confirm("Are you sure you want to delete all crew members? This action cannot be undone.").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep()
                            continue
                        db.crew.deleteall()
                        console.print("[green]All crew members deleted successfully.[/green]")
                        sleep(2)
                        continue
                    elif dopt == "Delete Specific Crew Member":
                        cid = questionary.text("Enter crew member ID to delete:").ask()
                        if not cid or not cid.isdigit() or int(cid) < 1 or cid not in [str(crew[0]) for crew in crew_list]:
                            console.print("[red]Invalid crew member ID. Please try again.[/red]")
                            sleep()
                            continue
                        cid = int(cid)
                        confirm = questionary.confirm(f"Are you sure you want to delete crew member ID {cid}?").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep()
                            continue
                        db.crew.delete(cid)
                        console.print(f"[green]Crew member ID {cid} deleted successfully.[/green]")
                        sleep(2)
                elif cchoice == "See All Crew Members":
                    clear()
                    crew_members = db.crew.fetchall()
                    if not crew_members:
                        console.print("[yellow]No crew members found.[/yellow]")
                    else:
                        console.print("[blue]Loading crew members...[/blue]")
                        table = Table(title="Crew Members")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Gender", style="green")
                        table.add_column("DOB", style="yellow")
                        table.add_column("Type", style="blue")
                        for member in crew_members:
                            table.add_row(str(member[0]), member[1], member[2], str(member[3]), member[4])
                        console.print(table)
                    input("Press Enter to continue...")
                elif cchoice == "Search Crew Member":
                    clear()
                    crew_members = db.crew.fetchall()
                    if not crew_members:
                        console.print("[yellow]No crew members found.[/yellow]")
                    else:
                        search_by = questionary.select(
                            "Search crew member by:",
                            choices=[
                                "ID",
                                "Name",
                                "Gender",
                                "CrewType",
                                "Status"
                            ]
                        ).ask()
                        if search_by == "ID":
                            cid = questionary.text("Enter crew member ID:").ask()
                            if not cid or not cid.isdigit():
                                console.print("[red]Invalid crew member ID. Please try again.[/red]")
                                sleep()
                                continue
                            cid = int(cid)
                            results = db.crew.search(cid)
                        else:
                            if search_by == "Gender":
                                search_key = questionary.select(
                                    "Select gender:",
                                    choices=[
                                        questionary.Choice(title="Male", value="M"),
                                        questionary.Choice(title="Female", value="F"),
                                        questionary.Choice(title="Other", value="O")
                                    ]
                                ).ask()
                            elif search_by == "CrewType":
                                crew_types = db.crew.availabletypes()
                                search_key = questionary.select(
                                    "Select crew type:",
                                    choices=[ct[0] for ct in crew_types]
                                ).ask()
                            else:
                                search_key = questionary.text(f"Enter crew member {search_by.lower()}:").ask()
                            if not search_key:
                                console.print(f"[red]{search_by} cannot be empty. Please try again.[/red]")
                                sleep()
                                continue
                            results = db.crew.searchby(search_by.lower(), search_key)
                        if not results:
                            console.print("[yellow]No matching crew members found.[/yellow]")
                        else:
                            console.print("[blue]Loading search results...[/blue]")
                            table = Table(title="Search Results")
                            table.add_column("ID", style="cyan", no_wrap=True)
                            table.add_column("Name", style="magenta")
                            table.add_column("Gender", style="green")
                            table.add_column("DOB", style="yellow")
                            table.add_column("Type", style="blue")
                            for member in results:
                                table.add_row(str(member[0]), member[1], member[2], str(member[3]), member[4])
                            console.print(table)
                    input("Press Enter to continue...")
                elif cchoice == "Crew Types":
                    clear()
                    types = db.crew.availabletypes()
                    if not types:
                        console.print("[yellow]No crew types found.[/yellow]")
                    else:
                        console.print("[blue]Loading crew types...[/blue]")
                        table = Table(title="Crew Types")
                        table.add_column("Type", style="cyan")
                        for t in types:
                            table.add_row(t[0])
                        console.print(table)
                    input("Press Enter to continue...")
                elif cchoice == "Crew Status":
                    clear()
                    stats = db.crew.fetchstats()
                    if not stats:
                        console.print("[yellow]No crew members found.[/yellow]")
                    else:
                        console.print("[blue]Loading crew status...[/blue]")
                        table = Table(title="Crew Status")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Status", style="green")
                        for s in stats:
                            table.add_row(str(s[0]), s[1], s[2])
                        console.print(table)
                    input("Press Enter to continue...")
        elif choice == "2":
            while True:
                clear()
                console.print("[bold blue]Naval Fleet Management System - Ship Management[/bold blue]")
                schoice =  questionary.select(
                    "Ship Menu - Select an option:",
                    choices=[
                        questionary.Choice(title=[("class:blue", "Add Ship")], value="Add Ship"),
                        questionary.Choice(title=[("class:magenta", "Update Ship")], value="Update Ship"),
                        questionary.Choice(title=[("class:yellow", "Delete Ship")], value="Delete Ship"),
                        questionary.Choice(title=[("class:green", "See All Ships")], value="See All Ships"),
                        questionary.Choice(title=[("class:bright_blue", "Search Ship")], value="Search Ship"),
                        questionary.Choice(title=[("class:bright_magenta", "Ship Types")], value="Ship Types"),
                        questionary.Choice(title=[("class:bright_green", "Ship Classes")], value="Ship Classes"),
                        questionary.Choice(title=[("class:bright_yellow", "Ship Status")], value="Ship Status"),
                        questionary.Choice(title=[("class:bright_cyan", "Ship Locations")], value="Ship Locations"),
                        questionary.Choice(title=[("class:bright_green", "Docked Ships")], value="Docked Ships"),
                        questionary.Choice(title=[("class:yellow", "Undocked Ships")], value="Undocked Ships"),
                        questionary.Choice(title=[("class:exit", "Back to Main Menu")], value="Back to Main Menu"),
                    ], style=custom_style
                ).ask()
                if schoice == "Back to Main Menu":
                    break
                elif schoice == "Add Ship":
                    clear()
                    sname = questionary.text("Enter ship name:").ask()
                    sclass = questionary.text("Enter ship class:").ask()
                    spennant = questionary.text("Enter ship pennant number:").ask()
                    stype = questionary.text("Enter ship type (e.g., Destroyer, Frigate):").ask()
                    sstatus = questionary.select(
                        "Select ship status:",
                        choices=["Active", "Inactive", "Under Maintenance", "Decommissioned"]
                    ).ask()
                    slocation = questionary.text("Enter ship location (e.g., Base name or coordinates):").ask()
                    sdockstatus = questionary.select(
                        "Select dock status:",
                        choices=[
                            questionary.Choice(title="Docked", value="d"),
                            questionary.Choice(title="Undocked", value="u")
                        ]
                    ).ask()
                    if not all([sname, sclass, spennant, stype, sstatus, slocation, sdockstatus]):
                        console.print("[red]All fields are required. Please try again.[/red]")
                        sleep()
                        continue
                    try:
                        db.ship.add(sname, sclass, spennant, stype, sstatus, slocation, sdockstatus)
                    except Exception as e:
                        console.print(f"[red]Error adding ship: {e}[/red]")
                        sleep()
                        continue
                    console.print(f"[green]Ship {sname} added successfully.[/green]")
                    sleep(2)
                elif schoice == "Update Ship":
                    clear()
                    if not db.ship.fetchall():
                        console.print("[yellow]No ships found to update.[/yellow]")
                        sleep()
                        continue
                    ship_list = db.ship.fetchall()
                    sid = questionary.text("Enter ship ID to update:").ask()
                    if not sid or not sid.isdigit() or int(sid) < 1 or sid not in [str(ship[0]) for ship in ship_list]:
                        console.print("[red]Invalid ship ID. Please try again.[/red]")
                        sleep()
                        continue
                    sid = int(sid)
                    sname = questionary.text("Enter new name (leave blank to keep current):").ask()
                    sclass = questionary.text("Enter new class (leave blank to keep current):").ask()
                    spennant = questionary.text("Enter new pennant number (leave blank to keep current):").ask()
                    stype = questionary.text("Enter new type (leave blank to keep current):").ask()
                    sstatus = questionary.select(
                        "Select status:",
                        choices=[
                            "Active",
                            "Inactive",
                            "Under Maintenance",
                            "Decommissioned",
                            "Keep current"
                        ]
                    ).ask()
                    if sstatus == "Keep current":
                        sstatus = None
                    slocation = questionary.text("Enter new location (leave blank to keep current):").ask()
                    sdockstatus = questionary.select(
                        "Select dock status:",
                        choices=[
                            questionary.Choice(title="Docked", value="d"),
                            questionary.Choice(title="Undocked", value="u"),
                            "Keep current"
                        ]
                    ).ask()
                    if sdockstatus == "Keep current":
                        sdockstatus = None
                    if not any([sname, sclass, spennant, stype, sstatus, slocation, sdockstatus]):
                        console.print("[red]No updates provided. Please try again.[/red]")
                        sleep()
                        continue
                    try:
                        db.ship.update(sid, name=sname if sname else None, shipclass=sclass if sclass else None, pennanto=spennant if spennant else None, type=stype if stype else None, status=sstatus, location=slocation if slocation else None, DockStatus=sdockstatus)
                    except Exception as e:
                        console.print(f"[red]Error updating ship: {e}[/red]")
                        sleep()
                        continue
                    console.print(f"[green]Ship ID {sid} updated successfully.[/green]")
                    sleep(2)
                elif schoice == "Delete Ship":
                    clear()
                    if not db.ship.fetchall():
                        console.print("[yellow]No ships found to delete.[/yellow]")
                        sleep()
                        continue
                    ship_list = db.ship.fetchall()
                    dopt = questionary.select(
                        "Delete Options:",
                        choices=[
                            "Delete All Ships",
                            "Delete Specific Ship",
                            "Cancel"
                        ]
                    ).ask()
                    if dopt == "Cancel":
                        console.print("[yellow]Deletion cancelled.[/yellow]")
                        sleep()
                        continue
                    elif dopt == "Delete All Ships":
                        confirm = questionary.confirm("Are you sure you want to delete all ships? This action cannot be undone.").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep()
                            continue
                        db.ship.deleteall()
                        console.print("[green]All ships deleted successfully.[/green]")
                        sleep(2)
                        continue
                    elif dopt == "Delete Specific Ship":
                        sid = questionary.text("Enter ship ID to delete:").ask()
                        if not sid or not sid.isdigit() or int(sid) < 1 or sid not in [str(ship[0]) for ship in ship_list]:
                            console.print("[red]Invalid ship ID. Please try again.[/red]")
                            sleep()
                            continue
                        sid = int(sid)
                        confirm = questionary.confirm(f"Are you sure you want to delete ship ID {sid}?").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep()
                            continue
                        db.ship.delete(sid)
                        console.print(f"[green]Ship ID {sid} deleted successfully.[/green]")
                        sleep(2)
                elif schoice == "See All Ships":
                    clear()
                    ships = db.ship.fetchall()
                    if not ships:
                        console.print("[yellow]No ships found.[/yellow]")
                    else:
                        console.print("[blue]Loading ships...[/blue]")
                        table = Table(title="Ships")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Class", style="green")
                        table.add_column("Pennant Number", style="yellow")
                        table.add_column("Type", style="blue")
                        for ship in ships:
                            table.add_row(str(ship[0]), ship[1], ship[2], ship[3], ship[4])
                        console.print(table)
                    input("Press Enter to continue...")
                elif schoice == "Search Ship":
                    clear()
                    ships = db.ship.fetchall()
                    if not ships:
                        console.print("[yellow]No ships found.[/yellow]")
                    else:
                        search_by = questionary.select(
                            "Search ship by:",
                            choices=[
                                "ID",
                                "Name",
                                "Class",
                                "PenantNumber",
                                "ShipType"
                            ]
                        ).ask()
                        if search_by == "ID":
                            sid = questionary.text("Enter ship ID:").ask()
                            if not sid or not sid.isdigit():
                                console.print("[red]Invalid ship ID. Please try again.[/red]")
                                sleep()
                                continue
                            sid = int(sid)
                            results = db.ship.search(sid)
                        else:
                            if search_by == "Class":
                                ship_classes = db.ship.availableclasses()
                                search_key = questionary.select(
                                    "Select ship class:",
                                    choices=[sc[0] for sc in ship_classes]
                                ).ask()
                            elif search_by == "ShipType":
                                ship_types = db.ship.availabletypes()
                                search_key = questionary.select(
                                    "Select ship type:",
                                    choices=[st[0] for st in ship_types]
                                ).ask()
                            else:
                                search_key = questionary.text(f"Enter ship {search_by.lower()}:").ask()
                            if not search_key:
                                console.print(f"[red]{search_by} cannot be empty. Please try again.[/red]")
                                sleep()
                                continue
                            results = db.ship.searchby(search_by.lower(), search_key)
                        if not results:
                            console.print("[yellow]No matching ships found.[/yellow]")
                        else:
                            console.print("[blue]Loading search results...[/blue]")
                            table = Table(title="Search Results")
                            table.add_column("ID", style="cyan", no_wrap=True)
                            table.add_column("Name", style="magenta")
                            table.add_column("Class", style="green")
                            table.add_column("Pennant Number", style="yellow")
                            table.add_column("Type", style="blue")
                            for ship in results:
                                table.add_row(str(ship[0]), ship[1], ship[2], ship[3], ship[4])
                            console.print(table)
                    input("Press Enter to continue...")
                elif schoice == "Ship Types":
                    clear()
                    types = db.ship.availabletypes()
                    if not types:
                        console.print("[yellow]No ship types found.[/yellow]")
                    else:
                        console.print("[blue]Loading ship types...[/blue]")
                        table = Table(title="Ship Types")
                        table.add_column("Type", style="cyan")
                        for t in types:
                            table.add_row(t[0])
                        console.print(table)
                    input("Press Enter to continue...")
                elif schoice == "Ship Classes":
                    clear()
                    classes = db.ship.availableclasses()
                    if not classes:
                        console.print("[yellow]No ship classes found.[/yellow]")
                    else:
                        console.print("[blue]Loading ship classes...[/blue]")
                        table = Table(title="Ship Classes")
                        table.add_column("Class", style="cyan")
                        for c in classes:
                            table.add_row(c[0])
                        console.print(table)
                    input("Press Enter to continue...")
                elif schoice == "Ship Status":
                    clear()
                    stats = db.ship.fetchstats()
                    if not stats:
                        console.print("[yellow]No ships found.[/yellow]")
                    else:
                        console.print("[blue]Loading ship status...[/blue]")
                        table = Table(title="Ship Status")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Pennant Number", style="yellow")
                        table.add_column("Status", style="green")
                        for s in stats:
                            table.add_row(str(s[0]), s[1], s[2], s[3])
                        console.print(table)
                    input("Press Enter to continue...")
                elif schoice == "Ship Locations":
                    clear()
                    locs = db.ship.fetchlocation()
                    if not locs:
                        console.print("[yellow]No ships found.[/yellow]")
                    else:
                        console.print("[blue]Loading ship locations...[/blue]")
                        table = Table(title="Ship Locations")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Pennant Number", style="yellow")
                        table.add_column("Location", style="green")
                        for l in locs:
                            table.add_row(str(l[0]), l[1], l[2], l[3])
                        console.print(table)
                    input("Press Enter to continue...")
                elif schoice == "Docked Ships":
                    clear()
                    docked = db.ship.fetchdocked()
                    if not docked:
                        console.print("[yellow]No docked ships found.[/yellow]")
                    else:
                        console.print("[blue]Loading docked ships...[/blue]")
                        table = Table(title="Docked Ships")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Pennant Number", style="yellow")
                        for d in docked:
                            table.add_row(str(d[0]), d[1], d[2])
                        console.print(table)
                    input("Press Enter to continue...")
                elif schoice == "Undocked Ships":
                    clear()
                    undocked = db.ship.fetchundocked()
                    if not undocked:
                        console.print("[yellow]No undocked ships found.[/yellow]")
                    else:
                        console.print("[blue]Loading undocked ships...[/blue]")
                        table = Table(title="Undocked Ships")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Pennant Number", style="yellow")
                        for u in undocked:
                            table.add_row(str(u[0]), u[1], u[2])
                        console.print(table)
                    input("Press Enter to continue...")
        elif choice == "3":
             while True:
                clear()
                console.print("[bold blue]Naval Fleet Management System - Mission Management[/bold blue]")
                mchoice =  questionary.select(
                    "Mission Menu - Select an option:",
                    choices=[
                        questionary.Choice(title=[("class:blue", "Current Missions")], value="Current Missions"),
                        questionary.Choice(title=[("class:magenta", "Executed Missions")], value="Executed Missions"),
                        questionary.Choice(title=[("class:yellow", "Planned Missions")], value="Planned Missions"),
                        questionary.Choice(title=[("class:green", "Mission Planner")], value="Mission Planner"),
                        questionary.Choice(title=[("class:bright_blue", "Mission Controller")], value="Mission Controller"),
                        questionary.Choice(title=[("class:exit", "Back to Main Menu")], value="Back to Main Menu"),
                    ], style=custom_style
                ).ask()
                if mchoice == "Back to Main Menu":
                    break
                elif mchoice == "Current Missions":
                    clear()
                    current = db.mission.planner.fetchongoing()
                    if not current:
                        console.print("[yellow]No current missions found.[/yellow]")
                    else:
                        console.print("[blue]Loading current missions...[/blue]")
                        table = Table(title="Current Missions")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Type", style="green")
                        table.add_column("Objective", style="yellow")
                        table.add_column("Duration", style="blue")
                        table.add_column("Start Date", style="bright_green")
                        table.add_column("End Date", style="bright_yellow")
                        table.add_column("Status", style="bright_cyan")
                        for m in current:
                            table.add_row(str(m[0]), m[1], m[2], m[3], str(m[4]), str(m[5]), str(m[6]), m[7])
                        console.print(table)
                    input("Press Enter to continue...")
                elif mchoice == "Executed Missions":
                    clear()
                    executed = db.mission.planner.fetchexecuted()
                    if not executed:
                        console.print("[yellow]No executed missions found.[/yellow]")
                    else:
                        console.print("[blue]Loading executed missions...[/blue]")
                        table = Table(title="Executed Missions")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Type", style="green")
                        table.add_column("Objective", style="yellow")
                        table.add_column("Duration", style="blue")
                        table.add_column("Start Date", style="bright_green")
                        table.add_column("End Date", style="bright_yellow")
                        table.add_column("Status", style="bright_cyan")
                        for m in executed:
                            table.add_row(str(m[0]), m[1], m[2], m[3], str(m[4]), str(m[5]), str(m[6]), m[7])
                        console.print(table)
                    input("Press Enter to continue...")
                elif mchoice == "Planned Missions":
                    clear()
                    planned = db.mission.planner.fetchplanned()
                    if not planned:
                        console.print("[yellow]No planned missions found.[/yellow]")
                    else:
                        console.print("[blue]Loading planned missions...[/blue]")
                        table = Table(title="Planned Missions")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Type", style="green")
                        table.add_column("Objective", style="yellow")
                        table.add_column("Duration", style="blue")
                        table.add_column("Start Date", style="bright_green")
                        table.add_column("End Date", style="bright_yellow")
                        table.add_column("Status", style="bright_cyan")
                        for m in planned:
                            table.add_row(str(m[0]), m[1], m[2], m[3], str(m[4]), str(m[5]), str(m[6]), m[7])
                        console.print(table)
                    input("Press Enter to continue...")
                elif mchoice == "Mission Planner":
                    while True:
                        clear()
                        console.print("[bold blue]Naval Fleet Management System - Mission Planner[/bold blue]")
                        mpchoice =  questionary.select(
                            "Mission Planner - Select an option:",
                            choices=[
                                questionary.Choice(title=[("class:blue", "Plan Mission")], value="Plan Mission"),
                                questionary.Choice(title=[("class:magenta", "Delete Mission")], value="Delete Mission"),
                                questionary.Choice(title=[("class:yellow", "See All Missions")], value="See All Missions"),
                                questionary.Choice(title=[("class:green", "Search Mission")], value="Search Mission"),
                                questionary.Choice(title=[("class:exit", "Back to Mission Menu")], value="Back to Mission Menu"),
                            ], style=custom_style
                        ).ask()
                        if mpchoice == "Back to Mission Menu":
                            break
                        elif mpchoice == "Plan Mission":
                            clear()
                            mname = questionary.text("Enter mission name:").ask()
                            mtype = questionary.text("Enter mission type (e.g., Reconnaissance, Combat):").ask()
                            mobjective = questionary.text("Enter mission objective:").ask()
                            mduration = questionary.text("Enter mission duration (in days) (optional):").ask()
                            mstartdate = questionary.text("Enter mission start date (YYYY-MM-DD) (optional):").ask()
                            menddate = questionary.text("Enter mission end date (YYYY-MM-DD) (optional):").ask()
                            if not all([mname, mtype, mobjective]):
                                console.print("[red]Few fields are required. Please try again.[/red]")
                                sleep()
                                continue
                            if mduration:
                                if not mduration.isdigit() or int(mduration) < 1:
                                    console.print("[red]Duration must be a positive integer. Please try again.[/red]")
                                    sleep()
                                    continue
                                mduration = int(mduration)
                            else:
                                mduration = None
                            if not mstartdate:
                                mstartdate = None
                            if not menddate:
                                menddate = None
                            try:
                                db.mission.planner.plan_mission(mname, mtype, mobjective, mduration, mstartdate, menddate)
                            except Exception as e:
                                console.print(f"[red]Error planning mission: {e}[/red]")
                                sleep()
                                continue
                            console.print(f"[green]Mission {mname} planned successfully.[/green]")
                            sleep(2)
                        elif mpchoice == "Delete Mission":
                            clear()
                            if not db.mission.planner.fetchall():
                                console.print("[yellow]No missions found to delete.[/yellow]")
                                sleep()
                                continue
                            mission_list = db.mission.planner.fetchall()
                            dopt = questionary.select(
                                "Delete Options:",
                                choices=[
                                    "Delete All Missions",
                                    "Delete Specific Mission",
                                    "Cancel"
                                ]
                            ).ask()
                            if dopt == "Cancel":
                                console.print("[yellow]Deletion cancelled.[/yellow]")
                                sleep()
                                continue
                            elif dopt == "Delete All Missions":
                                confirm = questionary.confirm("Are you sure you want to delete all missions? This action cannot be undone.").ask()
                                if not confirm:
                                    console.print("[yellow]Deletion cancelled.[/yellow]")
                                    sleep()
                                    continue
                                db.mission.planner.deleteall()
                                console.print("[green]All missions deleted successfully.[/green]")
                                sleep(2)
                                continue
                            elif dopt == "Delete Specific Mission":
                                mid = questionary.text("Enter mission ID to delete:").ask()
                                if not mid or not mid.isdigit() or int(mid) < 1 or mid not in [str(mission[0]) for mission in mission_list]:
                                    console.print("[red]Invalid mission ID. Please try again.[/red]")
                                    sleep()
                                    continue
                                mid = int(mid)
                                confirm = questionary.confirm(f"Are you sure you want to delete mission ID {mid}?").ask()
                                if not confirm:
                                    console.print("[yellow]Deletion cancelled.[/yellow]")
                                    sleep()
                                    continue
                                db.mission.planner.delete_mission(mid)
                                console.print(f"[green]Mission ID {mid} deleted successfully.[/green]")
                                sleep(2)
                        elif mpchoice == "See All Missions":
                            clear()
                            missions = db.mission.planner.fetchall()
                            if not missions:
                                console.print("[yellow]No missions found.[/yellow]")
                            else:
                                console.print("[blue]Loading missions...[/blue]")
                                table = Table(title="Missions")
                                table.add_column("ID", style="cyan", no_wrap=True)
                                table.add_column("Name", style="magenta")
                                table.add_column("Type", style="green")
                                table.add_column("Objective", style="yellow")
                                table.add_column("Duration", style="blue")
                                table.add_column("Start Date", style="bright_green")
                                table.add_column("End Date", style="bright_yellow")
                                table.add_column("Status", style="bright_cyan")
                                for m in missions:
                                    table.add_row(str(m[0]), m[1], m[2], m[3], str(m[4]), str(m[5]), str(m[6]), m[7])
                                console.print(table)
                            input("Press Enter to continue...")
                        elif mpchoice == "Search Mission":
                            clear()
                            missions = db.mission.planner.fetchall()
                            if not missions:
                                console.print("[yellow]No missions found.[/yellow]")
                            else:
                                search_by = questionary.select(
                                    "Search mission by:",
                                    choices=[
                                        "ID",
                                        "Name",
                                        "MissionType",
                                        "Objective",
                                        "Status"
                                    ]
                                ).ask()
                                if search_by == "ID":
                                    mid = questionary.text("Enter mission ID:").ask()
                                    if not mid or not mid.isdigit():
                                        console.print("[red]Invalid mission ID. Please try again.[/red]")
                                        sleep()
                                        continue
                                    mid = int(mid)
                                    results = db.mission.planner.search(mid)
                                else:
                                    if search_by == "MissionType":
                                        mission_types = db.mission.planner.availabletypes()
                                        search_key = questionary.select(
                                            "Select mission type:",
                                            choices=[mt[0] for mt in mission_types]
                                        ).ask()
                                    elif search_by == "Status":
                                        mission_statuses = db.mission.planner.availablestatuses()
                                        search_key = questionary.select(
                                            "Select mission status:",
                                            choices=[ms[0] for ms in mission_statuses]
                                        ).ask()
                                    else:
                                        search_key = questionary.text(f"Enter mission {search_by.lower()}:").ask()
                                    if not search_key:
                                        console.print(f"[red]{search_by} cannot be empty. Please try again.[/red]")
                                        sleep()
                                        continue
                                    results = db.mission.planner.searchby(search_by.lower(), search_key)
                                if not results:
                                    console.print("[yellow]No matching missions found.[/yellow]")
                                else:
                                    console.print("[blue]Loading search results...[/blue]")
                                    table = Table(title="Search Results")
                                    table.add_column("ID", style="cyan", no_wrap=True)
                                    table.add_column("Name", style="magenta")
                                    table.add_column("Type", style="green")
                                    table.add_column("Objective", style="yellow")
                                    table.add_column("Duration", style="blue")
                                    table.add_column("Start Date", style="bright_green")
                                    table.add_column("End Date", style="bright_yellow")
                                    table.add_column("Status", style="bright_cyan")
                                    for m in results:
                                        table.add_row(str(m[0]), m[1], m[2], m[3], str(m[4]), str(m[5]), str(m[6]), m[7])
                                    console.print(table)
                            input("Press Enter to continue...")
                elif mchoice == "Mission Controller":
                    while True:
                        clear()
                        console.print("[bold blue]Naval Fleet Management System - Mission Controller[/bold blue]")
                        mcchoice =  questionary.select(
                            "Mission Controller - Select an option:",
                            choices=[
                                questionary.Choice(title=[("class:blue", "Start Mission")], value="Start Mission"),
                                questionary.Choice(title=[("class:magenta", "End Mission")], value="End Mission"),
                                questionary.Choice(title=[("class:yellow", "Abort Mission")], value="Abort Mission"),
                                questionary.Choice(title=[("class:green", "Pause Mission")], value="Pause Mission"),
                                questionary.Choice(title=[("class:bright_blue", "Modify Mission")], value="Modify Mission"),
                                questionary.Choice(title=[("class:exit", "Back to Mission Menu")], value="Back to Mission Menu"),
                            ], style=custom_style
                        ).ask()
                        if mcchoice == "Back to Mission Menu":
                            break
                        elif mcchoice == "Start Mission":
                            clear()
                            planned = db.mission.planner.fetchplanned()
                            if not planned:
                                console.print("[yellow]No planned or Paused missions available to start.[/yellow]")
                                sleep()
                                continue
                            mid = questionary.text("Enter mission ID to start:").ask()
                            if not mid or not mid.isdigit() or int(mid) < 1:
                                console.print("[red]Invalid mission ID. Please try again.[/red]")
                                sleep()
                                continue
                            mid = int(mid)
                            ships = db.ship.fetchall()
                            if not ships:
                                console.print("[yellow]No ships available to assign to the mission.[/yellow]")
                                sleep()
                                continue
                            ship_ids = questionary.text("Enter comma-separated ship IDs to assign to the mission:").ask()
                            if not ship_ids:
                                console.print("[red]At least one ship ID is required. Please try again.[/red]")
                                sleep()
                                continue
                            try:
                                ship_ids = [int(sid.strip()) for sid in ship_ids.split(",") if sid.strip().isdigit() and int(sid.strip()) > 0]
                                if not ship_ids:
                                    raise ValueError
                            except ValueError:
                                console.print("[red]Invalid ship IDs. Please try again.[/red]")
                                sleep()
                                continue
                            try:
                                db.mission.controller.start_mission(mid, ship_ids)
                            except Exception as e:
                                console.print(f"[red]Error starting mission: {e}[/red]")
                                sleep()
                                continue
                            console.print(f"[green]Mission ID {mid} started successfully with ships {', '.join(map(str, ship_ids))}.[/green]")
                            sleep(2)
                        elif mcchoice == "End Mission":
                            clear()
                            current = db.mission.planner.fetchongoing()
                            if not current:
                                console.print("[yellow]No ongoing missions available to end.[/yellow]")
                                sleep()
                                continue
                            mid = questionary.text("Enter mission ID to end:").ask()
                            if not mid or not mid.isdigit() or int(mid) < 1 or int(mid) > len(current):
                                console.print("[red]Invalid mission ID. Please try again.[/red]")
                                sleep()
                                continue
                            mid = int(mid)
                            shipids = []
                            for m in current:
                                if m[0] == mid:
                                    shipids = [int(sid) for sid in m[7].split() if sid.isdigit()]
                                    break
                            try:
                                db.mission.controller.end_mission(mid, shipids)
                            except Exception as e:
                                console.print(f"[red]Error ending mission: {e}[/red]")
                                sleep()
                                continue
                            console.print(f"[green]Mission ID {mid} ended successfully.[/green]")
                            sleep(2)
                        elif mcchoice == "Abort Mission":
                            clear()
                            current = db.mission.planner.fetchongoing()
                            if not current:
                                console.print("[yellow]No ongoing missions available to abort.[/yellow]")
                                sleep()
                                continue
                            mid = questionary.text("Enter mission ID to abort:").ask()
                            if not mid or not mid.isdigit() or int(mid) < 1 or int(mid) > len(current):
                                console.print("[red]Invalid mission ID. Please try again.[/red]")
                                sleep()
                                continue
                            mid = int(mid)
                            shipids = []
                            for m in current:
                                if m[0] == mid:
                                    shipids = [int(sid) for sid in m[7].split() if sid.isdigit()]
                                    break
                            try:
                                db.mission.controller.abort_mission(mid, shipids)
                            except Exception as e:
                                console.print(f"[red]Error aborting mission: {e}[/red]")
                                sleep()
                                continue
                            console.print(f"[green]Mission ID {mid} aborted successfully.[/green]")
                            sleep(2)
                        elif mcchoice == "Pause Mission":
                            clear()
                            current = db.mission.planner.fetchongoing()
                            if not current:
                                console.print("[yellow]No ongoing missions available to pause.[/yellow]")
                                sleep()
                                continue
                            mid = questionary.text("Enter mission ID to pause:").ask()
                            if not mid or not mid.isdigit() or int(mid) < 1 or int(mid) > len(current):
                                console.print("[red]Invalid mission ID. Please try again.[/red]")
                                sleep()
                                continue
                            mid = int(mid)
                            try:
                                db.mission.controller.pause_mission(mid)
                            except Exception as e:
                                console.print(f"[red]Error pausing mission: {e}[/red]")
                                sleep()
                                continue
                            console.print(f"[green]Mission ID {mid} paused successfully.[/green]")
                            sleep(2)
                        elif mcchoice == "Modify Mission":
                            clear()
                            missions = db.mission.planner.fetchall()
                            if not missions:
                                console.print("[yellow]No missions found to modify.[/yellow]")
                                sleep()
                                continue
                            mid = questionary.text("Enter mission ID to modify:").ask()
                            if not mid or not mid.isdigit() or int(mid) < 1 or int(mid) > len(missions):
                                console.print("[red]Invalid mission ID. Please try again.[/red]")
                                sleep()
                                continue
                            mid = int(mid)
                            mname = questionary.text("Enter new mission name (leave blank to keep current):").ask()
                            mtype = questionary.text("Enter new mission type (leave blank to keep current):").ask()
                            mobjective = questionary.text("Enter new mission objective (leave blank to keep current):").ask()
                            mduration = questionary.text("Enter new mission duration in days (leave blank to keep current):").ask()
                            mstartdate = questionary.text("Enter new mission start date (YYYY-MM-DD) (leave blank to keep current):").ask()
                            menddate = questionary.text("Enter new mission end date (YYYY-MM-DD) (leave blank to keep current):").ask()
                            if mduration:
                                if not mduration.isdigit():
                                    console.print("[red]Invalid duration. Please try again.[/red]")
                                    sleep()
                                    continue
                            else:
                                mduration = None
                            if not mstartdate:
                                mstartdate = None
                            if not menddate:
                                menddate = None
                            try:
                                db.mission.controller.modifymission(mid, name=mname or None, type=mtype or None, objective=mobjective or None, duration=mduration, startdate=mstartdate, enddate=menddate)
                            except Exception as e:
                                console.print(f"[red]Error modifying mission: {e}[/red]")
                                sleep()
                                continue
                            console.print(f"[green]Mission ID {mid} modified successfully.[/green]")
                            sleep(2)
        elif choice == "4":
            clear()
            while True:
                console.print("[bold blue] Naval Fleet Management System - Document Management[/bold blue]")
                dchoice = questionary.select(
                    "Document Menu - Select an option:",
                    choices=[
                        questionary.Choice(title=[("class:blue", "Reports")], value="Reports"),
                        questionary.Choice(title=[("class:magenta", "Logs")], value="Logs"),
                        questionary.Choice(title=[("class:exit", "Back to Main Menu")], value="Back to Main Menu"),
                    ], style=custom_style
                ).ask()
                if dchoice == "Back to Main Menu":
                    break
                elif dchoice == "Reports":
                    while True:
                        clear()
                        console.print("[bold blue]Naval Fleet Management System - Reports[/bold blue]")
                        rchoice = questionary.select(
                            "Reports Menu - Select an option:",
                            choices=[
                                questionary.Choice(title=[("class:blue", "Create Report")], value="Create Report"),
                                questionary.Choice(title=[("class:magenta", "Read Report")], value="Read Report"),
                                questionary.Choice(title=[("class:yellow", "Show All Reports")], value="Show All Reports"),
                                questionary.Choice(title=[("class:green", "Search Reports")], value="Search Reports"),
                                questionary.Choice(title=[("class:bright_blue", "Delete Report")], value="Delete Report"),
                                questionary.Choice(title=[("class:exit", "Back to Document Menu")], value="Back to Document Menu"),
                            ], style=custom_style
                        ).ask()
                        if rchoice == "Back to Document Menu":
                            clear()
                            break
                        elif rchoice == "Create Report":
                            clear()
                            title = questionary.text("Enter report title:").ask()
                            description = questionary.text("Enter report description:").ask()
                            content = questionary.text("Enter report content:").ask()
                            document_type = questionary.select(
                                "Select document type:",
                                choices=[
                                    "Mission Report",
                                    "Maintenance Report",
                                    "Incident Report",
                                    "Other"
                                ]
                            ).ask()
                            if not all([title, description, content, document_type]):
                                console.print("[red]All fields are required. Please try again.[/red]")
                                sleep(2)
                                continue
                            try:
                                db.documents.reports.create_report(title, description, content, document_type)
                            except Exception as e:
                                console.print(f"[red]Error creating report: {e}[/red]")
                                sleep(2)
                                continue
                            console.print(f"[green]Report '{title}' created successfully.[/green]")
                            sleep(2)
                        elif rchoice == "Read Report":
                            clear()
                            rid = questionary.text("Enter report ID to read:").ask()
                            if not rid or not rid.isdigit() or int(rid) < 1:
                                console.print("[red]Invalid report ID. Please try again.[/red]")
                                sleep(2)
                                continue
                            rid = int(rid)
                            try:
                                report = db.documents.reports.read(rid)
                            except Exception as e:
                                console.print(f"[red]Error reading report: {e}[/red]")
                                sleep(2)
                                continue
                            if not report:
                                console.print("[yellow]No report found with the given ID.[/yellow]")
                            else:
                                r = report[0]
                                panel = Panel.fit(f"[bold blue]Title:[/bold blue] {r[1]}\n[bold blue]Description:[/bold blue] {r[2]}\n[bold blue]Content:[/bold blue]\n{r[3]}\n\n[bold magenta]Document Type:[/bold magenta] {r[4]}\n[bold magenta]Created At:[/bold magenta] {r[5]}", title=f"Report ID: {r[0]}", border_style="green")
                                console.print(panel)
                            input("Press Enter to continue...")
                        elif rchoice == "Show All Reports":
                            clear()
                            try:
                                reports = db.documents.reports.show_all()
                            except Exception as e:
                                console.print(f"[red]Error fetching reports: {e}[/red]")
                                sleep(2)
                                continue
                            if not reports:
                                console.print("[yellow]No reports found.[/yellow]")
                            else:
                                console.print("[blue]Loading reports...[/blue]")
                                table = Table(title="All Reports")
                                table.add_column("ID", style="cyan", no_wrap=True)
                                table.add_column("Title", style="magenta")
                                table.add_column("Description", style="green")
                                table.add_column("Document Type", style="yellow")
                                table.add_column("Created At", style="bright_green")
                                for r in reports:
                                    table.add_row(str(r[0]), r[1], r[2], r[3], str(r[4]))
                                console.print(table)
                            input("Press Enter to continue...")
                        elif rchoice == "Search Reports":
                            clear()
                            search_by = questionary.select(
                                "Search reports by:",
                                choices=[
                                    "Title",
                                    "Description",
                                    "DocumentType"
                                ]
                            ).ask()
                            if search_by == "DocumentType":
                                doc_types = db.documents.reports.available_types()
                                search_key = questionary.select(
                                    "Select document type:",
                                    choices=[dt[0] for dt in doc_types]
                                ).ask()
                            else:
                                search_key = questionary.text(f"Enter report {search_by.lower()}:").ask()
                            if not search_key:
                                console.print(f"[red]{search_by} cannot be empty. Please try again.[/red]")
                                sleep(2)
                                continue
                            try:
                                results = db.documents.reports.search(search_by.lower(), search_key)
                            except Exception as e:
                                console.print(f"[red]Error searching reports: {e}[/red]")
                                sleep(2)
                                continue
                            if not results:
                                console.print("[yellow]No matching reports found.[/yellow]")
                            else:
                                console.print("[blue]Loading search results...[/blue]")
                                table = Table(title="Search Results")
                                table.add_column("ID", style="cyan", no_wrap=True)
                                table.add_column("Title", style="magenta")
                                table.add_column("Description", style="green")
                                table.add_column("Document Type", style="yellow")
                                table.add_column("Created At", style="bright_green")
                                for r in results:
                                    table.add_row(str(r[0]), r[1], r[2], r[3], str(r[4]))
                                console.print(table)
                            input("Press Enter to continue...")
                        elif rchoice == "Delete Report":
                            clear()
                            reports = db.documents.reports.show_all()
                            if not reports:
                                console.print("[yellow]No reports found to delete.[/yellow]")
                                sleep(2)
                                continue
                            dopt = questionary.select(
                                "Delete Options:",
                                choices=[
                                    "Delete All Reports",
                                    "Delete Specific Report",
                                    "Cancel"
                                ]
                            ).ask()
                            if dopt == "Cancel":
                                console.print("[yellow]Deletion cancelled.[/yellow]")
                                sleep(2)
                                continue
                            elif dopt == "Delete All Reports":
                                clear()
                                confirm = questionary.confirm("Are you sure you want to delete all reports? This action cannot be undone.").ask()
                                if not confirm:
                                    console.print("[yellow]Deletion cancelled.[/yellow]")
                                    sleep(2)
                                    continue
                                try:
                                    db.documents.reports.delete_all()
                                except Exception as e:
                                    console.print(f"[red]Error deleting reports: {e}[/red]")
                                    sleep(2)
                                    continue
                                console.print("[green]All reports deleted successfully.[/green]")
                                sleep(2)
                                continue
                            elif dopt == "Delete Specific Report":
                                clear()
                                rid = questionary.text("Enter report ID to delete:").ask()
                                if not rid or not rid.isdigit() or int(rid) < 1 or rid not in [str(r[0]) for r in reports]:
                                    console.print("[red]Invalid report ID. Please try again.[/red]")
                                    sleep(2)
                                    continue
                                rid = int(rid)
                                confirm = questionary.confirm(f"Are you sure you want to delete report ID {rid}?").ask()
                                if not confirm:
                                    console.print("[yellow]Deletion cancelled.[/yellow]")
                                    sleep(2)
                                    continue
                                try:
                                    db.documents.reports.delete(rid)
                                except Exception as e:
                                    console.print(f"[red]Error deleting report: {e}[/red]")
                                    sleep(2)
                                    continue
                                console.print(f"[green]Report ID {rid} deleted successfully.[/green]")
                                sleep(2)
                elif dchoice == "Logs":
                    while True:
                        clear()
                        console.print("[bold blue]Naval Fleet Management System - Logs[/bold blue]")
                        lchoice = questionary.select(
                            "Logs Menu - Select an option:",
                            choices=[
                                questionary.Choice(title=[("class:blue", "Add Log Entry")], value="Add Log Entry"),
                                questionary.Choice(title=[("class:magenta", "Read Log Entry")], value="Read Log Entry"),
                                questionary.Choice(title=[("class:yellow", "Read All Logs")], value="Read All Logs"),
                                questionary.Choice(title=[("class:exit", "Back to Document Menu")], value="Back to Document Menu"),
                            ], style=custom_style
                        ).ask()
                        if lchoice == "Back to Document Menu":
                            clear()
                            break
                        elif lchoice == "Add Log Entry":
                            clear()
                            title = questionary.text("Enter log title:").ask()
                            description = questionary.text("Enter log description:").ask()
                            if not all([title, description]):
                                console.print("[red]All fields are required. Please try again.[/red]")
                                sleep(2)
                                continue
                            try:
                                db.documents.logs.add(title, description)
                            except Exception as e:
                                console.print(f"[red]Error adding log entry: {e}[/red]")
                                sleep(2)
                                continue
                            console.print(f"[green]Log entry '{title}' added successfully.[/green]")
                            sleep(2)
                        elif lchoice == "Read Log Entry":
                            clear()
                            lid = questionary.text("Enter log ID to read:").ask()
                            if not lid or not lid.isdigit() or int(lid) < 1:
                                console.print("[red]Invalid log ID. Please try again.[/red]")
                                sleep(2)
                                continue
                            lid = int(lid)
                            try:
                                log = db.documents.logs.read(lid)
                            except Exception as e:
                                console.print(f"[red]Error reading log entry: {e}[/red]")
                                sleep(2)
                                continue
                            if not log:
                                console.print("[yellow]No log entry found with the given ID.[/yellow]")
                            else:
                                l = log[0]
                                panel = Panel.fit(f"[bold blue]Title:[/bold blue] {l[1]}\n[bold blue]Description:[/bold blue]\n{l[2]}\n\n[bold magenta]Created At:[/bold megenta] {l[3]}", title=f"Log ID: {l[0]}", border_style="green")
                                console.print(panel)
                            input("Press Enter to continue...")
                        elif lchoice == "Read All Logs":
                            clear()
                            try:
                                logs = db.documents.logs.read_all()
                            except Exception as e:
                                console.print(f"[red]Error fetching logs: {e}[/red]")
                                sleep(2)
                                continue
                            if not logs:
                                console.print("[yellow]No log entries found.[/yellow]")
                            else:
                                console.print("[blue]Loading log entries...[/blue]")
                                panel = Panel.fit("\n".join(f"[bold magenta]{l[0]}[/bold magenta] [blue]{l[1]}[/blue] {l[2]} [bold magenta]{l[3]}[/bold magenta]" for l in logs), title="All Log Entries", border_style="green")
                                console.print(panel)
                            input("Press Enter to continue...")
        elif choice == "5":
            while True:
                clear()
                console.print("[bold blue]Naval Fleet Management System - Inventory Management[/bold blue]")
                invchoice = questionary.select(
                    "Inventory Menu - Select an option:",
                    choices=[
                        questionary.Choice(title=[("class:blue", "Add Item")], value="Add Item"),
                        questionary.Choice(title=[("class:magenta", "Update Item")], value="Update Item"),
                        questionary.Choice(title=[("class:yellow", "Delete Item")], value="Delete Item"),
                        questionary.Choice(title=[("class:green", "Show All Items")], value="Show All Items"),
                        questionary.Choice(title=[("class:bright_blue", "Search Items")], value="Search Items"),
                        questionary.Choice(title=[("class:bright_green", "See all Types")], value="See all Types"),
                        questionary.Choice(title=[("class:exit", "Back to Main Menu")], value="Back to Main Menu"),
                    ], style=custom_style
                ).ask()
                if invchoice == "Back to Main Menu":
                    clear()
                    break
                elif invchoice == "Add Item":
                    clear()
                    name = questionary.text("Enter item name:").ask()
                    category = questionary.select( "Select item category:",
                        choices = ["Missiles", "Launchers", "Aircrafts", "Air Defence Units", "Radar Stations", "Torpedoes", "Mines", "Vehicles", "Fuel", "Spare parts", "Other"]
                    ).ask()
                    quantity = questionary.text("Enter item quantity (optional):").ask()
                    if not quantity or not quantity.isdigit():
                        quantity = 0
                    if int(quantity) < 0:
                        console.print("[red]Invalid quantity. Please enter a non-negative integer.[/red]")
                        sleep(2)
                        continue
                    quantity = int(quantity)
                    if not all([name, category]):
                        console.print("[red]Few fields are required. Please try again.[/red]")
                        sleep(2)
                        continue
                    try:
                        db.inventory.add_item(name, category, quantity)
                    except Exception as e:
                        console.print(f"[red]Error adding item: {e}[/red]")
                        sleep(2)
                        continue
                    console.print(f"[green]Item '{name}' added successfully to inventory.[/green]")
                    sleep(2)
                elif invchoice == "Update Item":
                    clear()
                    items = db.inventory.fetch_all()
                    if not items:
                        console.print("[yellow]No items found to update.[/yellow]")
                        sleep(2)
                        continue
                    itemid = questionary.text("Enter item ID to update:").ask()
                    if not itemid or not itemid.isdigit() or int(itemid) < 1 or itemid not in [str(i[0]) for i in items]:
                        console.print("[red]Invalid item ID. Please try again.[/red]")
                        sleep(2)
                        continue
                    itemid = int(itemid)
                    name = questionary.text("Enter new item name (leave blank to keep current):").ask()
                    category = questionary.select(
                        "Select new item category (leave blank to keep current):",
                        choices=["Missiles", "Launchers", "Aircrafts", "Air Defence Units", "Radar Stations", "Torpedoes", "Mines", "Vehicles", "Fuel", "Spare parts", "Other", "Keep Current"]
                    ).ask()
                    if category == "Keep Current":
                        category = None
                    quantity = questionary.text("Enter new item quantity (leave blank to keep current):").ask()
                    if quantity:
                        if not quantity.isdigit() or int(quantity) < 0:
                            console.print("[red]Invalid quantity. Please enter a non-negative integer.[/red]")
                            sleep(2)
                            continue
                        quantity = int(quantity)
                    else:
                        quantity = None
                    if not any([name, category, quantity is not None]):
                        console.print("[red]At least one field must be updated. Please try again.[/red]")
                        sleep(2)
                        continue
                    try:
                        db.inventory.update_item(itemid, name=name or None, category=category, quantity=quantity)
                    except Exception as e:
                        console.print(f"[red]Error updating item: {e}[/red]")
                        sleep(2)
                        continue
                    console.print(f"[green]Item ID {itemid} updated successfully.[/green]")
                    sleep(2)
                elif invchoice == "Delete Item":
                    clear()
                    items = db.inventory.fetch_all()
                    if not items:
                        console.print("[yellow]No items found to delete.[/yellow]")
                        sleep(2)
                        continue
                    dopt = questionary.select(
                        "Delete Options:",
                        choices=[
                            "Delete All Items",
                            "Delete Specific Item",
                            "Cancel"
                        ]
                    ).ask()
                    if dopt == "Cancel":
                        console.print("[yellow]Deletion cancelled.[/yellow]")
                        sleep(2)
                        continue
                    elif dopt == "Delete All Items":
                        clear()
                        confirm = questionary.confirm("Are you sure you want to delete all items? This action cannot be undone.").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep(2)
                            continue
                        try:
                            db.inventory.delete_all()
                        except Exception as e:
                            console.print(f"[red]Error deleting items: {e}[/red]")
                            sleep(2)
                            continue
                        console.print("[green]All items deleted successfully.[/green]")
                        sleep(2)
                        continue
                    elif dopt == "Delete Specific Item":
                        clear()
                        itemid = questionary.text("Enter item ID to delete:").ask()
                        if not itemid or not itemid.isdigit() or int(itemid) < 1 or itemid not in [str(i[0]) for i in items]:
                            console.print("[red]Invalid item ID. Please try again.[/red]")
                            sleep(2)
                            continue
                        itemid = int(itemid)
                        confirm = questionary.confirm(f"Are you sure you want to delete item ID {itemid}?").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep(2)
                            continue
                        try:
                            db.inventory.delete_item(itemid)
                        except Exception as e:
                            console.print(f"[red]Error deleting item: {e}[/red]")
                            sleep(2)
                            continue
                        console.print(f"[green]Item ID {itemid} deleted successfully.[/green]")
                        sleep(2)
                elif invchoice == "Show All Items":
                    clear()
                    try:
                        items = db.inventory.fetch_all()
                    except Exception as e:
                        console.print(f"[red]Error fetching items: {e}[/red]")
                        sleep(2)
                        continue
                    if not items:
                        console.print("[yellow]No items found in inventory.[/yellow]")
                    else:
                        console.print("[blue]Loading inventory items...[/blue]")
                        table = Table(title="Inventory Items")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Category", style="green")
                        table.add_column("Quantity", style="yellow")
                        for i in items:
                            table.add_row(str(i[0]), i[1], i[2], str(i[3]))
                        console.print(table)
                    input("Press Enter to continue...")
                elif invchoice == "Search Items":
                    clear()
                    search_by = questionary.select(
                        "Search items by:",
                        choices=[
                            "Name",
                            "Category"
                        ]
                    ).ask()
                    if search_by == "Category":
                        categories = db.inventory.fetch_categories()
                        search_key = questionary.select(
                            "Select item category:",
                            choices=[cat[0] for cat in categories]
                        ).ask()
                    else:
                        search_key = questionary.text(f"Enter item {search_by.lower()}:").ask()
                    if not search_key:
                        console.print(f"[red]{search_by} cannot be empty. Please try again.[/red]")
                        sleep(2)
                        continue
                    try:
                        results = db.inventory.search(search_by.lower(), search_key)
                    except Exception as e:
                        console.print(f"[red]Error searching items: {e}[/red]")
                        sleep(2)
                        continue
                    if not results:
                        console.print("[yellow]No matching items found.[/yellow]")
                    else:
                        console.print("[blue]Loading search results...[/blue]")
                        table = Table(title="Search Results")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Category", style="green")
                        table.add_column("Quantity", style="yellow")
                        for i in results:
                            table.add_row(str(i[0]), i[1], i[2], str(i[3]))
                        console.print(table)
                    input("Press Enter to continue...")
                elif invchoice == "See all Types":
                    clear()
                    try:
                        categories = db.inventory.fetch_categories()
                    except Exception as e:
                        console.print(f"[red]Error fetching categories: {e}[/red]")
                        sleep(2)
                        continue
                    if not categories:
                        console.print("[yellow]No categories found in inventory.[/yellow]")
                    else:
                        console.print("[blue]Loading item categories...[/blue]")
                        panel = Panel.fit("\n".join(f"[bold magenta]{cat[0]}[/bold magenta]" for cat in categories), title="Item Categories", border_style="green")
                        console.print(panel)
                    input("Press Enter to continue...")
        elif choice == "6":
            while True:
                clear()
                console.print("[bold blue]Naval Fleet Management System - Base Management[/bold blue]")
                bchoice = questionary.select( "Base Menu - Select an option:",
                    choices = [
                        questionary.Choice(title=[("class:blue", "Add Base")], value="Add Base"),
                        questionary.Choice(title=[("class:magenta", "Update Base")], value="Update Base"),
                        questionary.Choice(title=[("class:yellow", "Delete Base")], value="Delete Base"),
                        questionary.Choice(title=[("class:green", "Show All Bases")], value="Show All Bases"),
                        questionary.Choice(title=[("class:bright_blue", "Search Bases")], value="Search Bases"),
                        questionary.Choice(title=[("class:bright_green", "See all Types")], value="See all Types"),
                        questionary.Choice(title=[("class:bright_cyan", "See all Status")], value="See all Status"),
                        questionary.Choice(title=[("class:exit", "Back to Main Menu")], value="Back to Main Menu"),
                    ],
                    style = custom_style
                ).ask()
                if bchoice == "Back to Main Menu":
                    clear()
                    break
                elif bchoice == "Add Base":
                    clear()
                    name = questionary.text("Enter base name:").ask()
                    location = questionary.text("Enter base location (optional):").ask()
                    if not location:
                        location = None
                    type = questionary.select(
                        "Select base type:",
                        choices=["Forward", "Secret", "Underwater", "Temporary", "Mainland", "Air bases", "Logistics Base", "Training Base", "Other"]
                    ).ask()
                    status = questionary.select(
                        "Select base status:",
                        choices=["Operational", "Not Operational", "Under Construction", "Decommissioned", "Other"]
                    ).ask()
                    if not all([name, type, status]):
                        console.print("[red]Few fields are required. Please try again.[/red]")
                        sleep(2)
                        continue
                    try:
                        db.bases.add_item(name, location, type, status)
                    except Exception as e:
                        console.print(f"[red]Error adding base: {e}[/red]")
                        sleep(2)
                        continue
                    console.print(f"[green]Base '{name}' added successfully.[/green]")
                    sleep(2)
                elif bchoice == "Update Base":
                    clear()
                    bases = db.bases.fetch_all()
                    if not bases:
                        console.print("[yellow]No bases found to update.[/yellow]")
                        sleep(2)
                        continue
                    bid = questionary.text("Enter base ID to update:").ask()
                    if not bid or not bid.isdigit() or int(bid) < 1 or bid not in [str(b[0]) for b in bases]:
                        console.print("[red]Invalid base ID. Please try again.[/red]")
                        sleep(2)
                        continue
                    bid = int(bid)
                    name = questionary.text("Enter new base name (leave blank to keep current):").ask()
                    location = questionary.text("Enter new base location (leave blank to keep current):").ask()
                    if not location:
                        location = None
                    type = questionary.select(
                        "Select new base type (leave blank to keep current):",
                        choices=["Forward", "Secret", "Underwater", "Temporary", "Mainland", "Air bases", "Logistics Base", "Training Base", "Other", "Keep Current"]
                    ).ask()
                    if type == "Keep Current":
                        type = None
                    status = questionary.select(
                        "Select new base status (leave blank to keep current):",
                        choices=["Operational", "Not Operational", "Under Construction", "Decommissioned", "Other", "Keep Current"]
                    ).ask()
                    if status == "Keep Current":
                        status = None
                    if not any([name, location, type, status]):
                        console.print("[red]At least one field must be updated. Please try again.[/red]")
                        sleep(2)
                        continue
                    try:
                        db.bases.update_item(bid, name=name or None, location=location, type=type, status=status)
                    except Exception as e:
                        console.print(f"[red]Error updating base: {e}[/red]")
                        sleep(2)
                        continue
                    console.print(f"[green]Base ID {bid} updated successfully.[/green]")
                    sleep(2)
                elif bchoice == "Delete Base":
                    clear()
                    bases = db.bases.fetch_all()
                    if not bases:
                        console.print("[yellow]No bases found to delete.[/yellow]")
                        sleep(2)
                        continue
                    dopt = questionary.select(
                        "Delete Options:",
                        choices=[
                            "Delete All Bases",
                            "Delete Specific Base",
                            "Cancel"
                        ]
                    ).ask()
                    if dopt == "Cancel":
                        console.print("[yellow]Deletion cancelled.[/yellow]")
                        sleep(2)
                        continue
                    elif dopt == "Delete All Bases":
                        clear()
                        confirm = questionary.confirm("Are you sure you want to delete all bases? This action cannot be undone.").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep(2)
                            continue
                        try:
                            db.bases.delete_all()
                        except Exception as e:
                            console.print(f"[red]Error deleting bases: {e}[/red]")
                            sleep(2)
                            continue
                        console.print("[green]All bases deleted successfully.[/green]")
                        sleep(2)
                        continue
                    elif dopt == "Delete Specific Base":
                        clear()
                        bid = questionary.text("Enter base ID to delete:").ask()
                        if not bid or not bid.isdigit() or int(bid) < 1 or bid not in [str(b[0]) for b in bases]:
                            console.print("[red]Invalid base ID. Please try again.[/red]")
                            sleep(2)
                            continue
                        bid = int(bid)
                        confirm = questionary.confirm(f"Are you sure you want to delete base ID {bid}?").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep(2)
                            continue
                        try:
                            db.bases.delete_item(bid)
                        except Exception as e:
                            console.print(f"[red]Error deleting base: {e}[/red]")
                            sleep(2)
                            continue
                        console.print(f"[green]Base ID {bid} deleted successfully.[/green]")
                        sleep(2)
                elif bchoice == "Show All Bases":
                    clear()
                    try:
                        bases = db.bases.fetch_all()
                    except Exception as e:
                        console.print(f"[red]Error fetching bases: {e}[/red]")
                        sleep(2)
                        continue
                    if not bases:
                        console.print("[yellow]No bases found.[/yellow]")
                    else:
                        console.print("[blue]Loading bases...[/blue]")
                        table = Table(title="All Bases")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Location", style="green")
                        table.add_column("Type", style="yellow")
                        table.add_column("Status", style="bright_green")
                        for b in bases:
                            loc = b[2] if b[2] else "N/A"
                            table.add_row(str(b[0]), b[1], loc, b[3], b[4])
                        console.print(table)
                    input("Press Enter to continue...")
                elif bchoice == "Search Bases":
                    clear()
                    search_by = questionary.select(
                        "Search bases by:",
                        choices=[
                            "Name",
                            "Location",
                            "Type",
                            "Status"
                        ]
                    ).ask()
                    if search_by in ["Type", "Status"]:
                        if search_by == "Type":
                            types = db.bases.fetchtypes()
                            search_key = questionary.select(
                                "Select base type:",
                                choices=[t[0] for t in types]
                            ).ask()
                        else:
                            statuses = db.bases.fetchstatuses()
                            search_key = questionary.select(
                                "Select base status:",
                                choices=[s[0] for s in statuses]
                            ).ask()
                    else:
                        search_key = questionary.text(f"Enter base {search_by.lower()}:").ask()
                    if not search_key:
                        console.print(f"[red]{search_by} cannot be empty. Please try again.[/red]")
                        sleep(2)
                        continue
                    try:
                        results = db.bases.search(search_by.lower(), search_key)
                    except Exception as e:
                        console.print(f"[red]Error searching bases: {e}[/red]")
                        sleep(2)
                        continue
                    if not results:
                        console.print("[yellow]No matching bases found.[/yellow]")
                    else:
                        console.print("[blue]Loading search results...[/blue]")
                        table = Table(title="Search Results")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Location", style="green")
                        table.add_column("Type", style="yellow")
                        table.add_column("Status", style="bright_green")
                        for b in results:
                            loc = b[2] if b[2] else "N/A"
                            table.add_row(str(b[0]), b[1], loc, b[3], b[4])
                        console.print(table)
                    input("Press Enter to continue...")
                elif bchoice == "See all Types":
                    clear()
                    try:
                        types = db.bases.fetchtypes()
                    except Exception as e:
                        console.print(f"[red]Error fetching types: {e}[/red]")
                        sleep(2)
                        continue
                    if not types:
                        console.print("[yellow]No base types found.[/yellow]")
                    else:
                        console.print("[blue]Loading base types...[/blue]")
                        panel = Panel.fit("\n".join(f"[bold magenta]{t[0]}[/bold magenta]" for t in types), title="Base Types", border_style="green")
                        console.print(panel)
                    input("Press Enter to continue...")
                elif bchoice == "See all Status":
                    clear()
                    try:
                        statuses = db.bases.fetchstatuses()
                    except Exception as e:
                        console.print(f"[red]Error fetching statuses: {e}[/red]")
                        sleep(2)
                        continue
                    if not statuses:
                        console.print("[yellow]No base statuses found.[/yellow]")
                    else:
                        console.print("[blue]Loading base statuses...[/blue]")
                        table = Table(title="Base Statuses")
                        table.add_column("BaseID", style="bright_green")
                        table.add_column("Base Name", style="magenta")
                        table.add_column("Status", style="yellow")
                        for s in statuses:
                            table.add_row(str(s[0]), s[1], s[2])
                        console.print(table)
                    input("Press Enter to continue...")
        elif choice == "7":
            while True:
                clear()
                console.print("[bold blue]Naval Fleet Management System - Route Management[/bold blue]")
                rchoice = questionary.select(
                    "Route Menu - Select an option:",
                    choices=[
                        questionary.Choice(title=[("class:blue", "Add Route")], value="Add Route"),
                        questionary.Choice(title=[("class:magenta", "Update Route")], value="Update Route"),
                        questionary.Choice(title=[("class:yellow", "Delete Route")], value="Delete Route"),
                        questionary.Choice(title=[("class:green", "Show All Routes")], value="Show All Routes"),
                        questionary.Choice(title=[("class:bright_blue", "View Route")], value="View Route"),
                        questionary.Choice(title=[("class:exit", "Back to Main Menu")], value="Back to Main Menu"),
                    ], style=custom_style
                ).ask()
                if rchoice == "Back to Main Menu":
                    clear()
                    break
                elif rchoice == "Add Route":
                    clear()
                    name = questionary.text("Enter route name:").ask()
                    origin = questionary.text("Enter route origin:").ask()
                    destination = questionary.text("Enter route destination:").ask()
                    waypoints = questionary.text("Enter waypoints (comma-separated, optional):").ask()
                    if not waypoints:
                        waypoints = None
                    distance = questionary.text("Enter route distance:").ask()
                    if not all([name, origin, destination, distance]):
                        console.print("[red]Few fields are required. Please try again.[/red]")
                        sleep(2)
                        continue
                    try:
                        db.routes.add(name, origin, destination, waypoints, distance)
                    except Exception as e:
                        console.print(f"[red]Error adding route: {e}[/red]")
                        sleep(2)
                        continue
                    console.print(f"[green]Route '{name}' added successfully.[/green]")
                    sleep(2)
                elif rchoice == "Update Route":
                    clear()
                    routes = db.routes.fetch_all()
                    if not routes:
                        console.print("[yellow]No routes found to update.[/yellow]")
                        sleep(2)
                        continue
                    rid = questionary.text("Enter route ID to update:").ask()
                    if not rid or not rid.isdigit() or int(rid) < 1 or rid not in [str(r[0]) for r in routes]:
                        console.print("[red]Invalid route ID. Please try again.[/red]")
                        sleep(2)
                        continue
                    rid = int(rid)
                    name = questionary.text("Enter new route name (leave blank to keep current):").ask()
                    origin = questionary.text("Enter new route origin (leave blank to keep current):").ask()
                    destination = questionary.text("Enter new route destination (leave blank to keep current):").ask()
                    waypoints = questionary.text("Enter new waypoints (comma-separated, leave blank to keep current):").ask()
                    if not waypoints:
                        waypoints = None
                    distance = questionary.text("Enter new route distance (leave blank to keep current):").ask()
                    if not any([name, origin, destination, waypoints, distance]):
                        console.print("[red]At least one field must be updated. Please try again.[/red]")
                        sleep(2)
                        continue
                    try:
                        db.routes.update(rid, name=name or None, startlocation=origin or None, endlocation=destination or None, waypoints=waypoints, distance=distance or None)
                    except Exception as e:
                        console.print(f"[red]Error updating route: {e}[/red]")
                        sleep(2)
                        continue
                    console.print(f"[green]Route ID {rid} updated successfully.[/green]")
                    sleep(2)
                elif rchoice == "Delete Route":
                    clear()
                    routes = db.routes.fetch_all()
                    if not routes:
                        console.print("[yellow]No routes found to delete.[/yellow]")
                        sleep(2)
                        continue
                    dopt = questionary.select(
                        "Delete Options:",
                        choices=[
                            "Delete All Routes",
                            "Delete Specific Route",
                            "Cancel"
                        ]
                    ).ask()
                    if dopt == "Cancel":
                        console.print("[yellow]Deletion cancelled.[/yellow]")
                        sleep(2)
                        continue
                    elif dopt == "Delete All Routes":
                        clear()
                        confirm = questionary.confirm("Are you sure you want to delete all routes? This action cannot be undone.").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep(2)
                            continue
                        try:
                            db.routes.delete_all()
                        except Exception as e:
                            console.print(f"[red]Error deleting routes: {e}[/red]")
                            sleep(2)
                            continue
                        console.print("[green]All routes deleted successfully.[/green]")
                        sleep(2)
                        continue
                    elif dopt == "Delete Specific Route":
                        clear()
                        rid = questionary.text("Enter route ID to delete:").ask()
                        if not rid or not rid.isdigit() or int(rid) < 1 or rid not in [str(r[0]) for r in routes]:
                            console.print("[red]Invalid route ID. Please try again.[/red]")
                            sleep(2)
                            continue
                        rid = int(rid)
                        confirm = questionary.confirm(f"Are you sure you want to delete route ID {rid}?").ask()
                        if not confirm:
                            console.print("[yellow]Deletion cancelled.[/yellow]")
                            sleep(2)
                            continue
                        try:
                            db.routes.delete(rid)
                        except Exception as e:
                            console.print(f"[red]Error deleting route: {e}[/red]")
                            sleep(2)
                            continue
                        console.print(f"[green]Route ID {rid} deleted successfully.[/green]")
                        sleep(2)
                elif rchoice == "Show All Routes":
                    clear()
                    try:
                        routes = db.routes.fetch_all()
                    except Exception as e:
                        console.print(f"[red]Error fetching routes: {e}[/red]")
                        sleep(2)
                        continue
                    if not routes:
                        console.print("[yellow]No routes found.[/yellow]")
                    else:
                        console.print("[blue]Loading routes...[/blue]")
                        table = Table(title="All Routes")
                        table.add_column("ID", style="cyan", no_wrap=True)
                        table.add_column("Name", style="magenta")
                        table.add_column("Origin", style="green")
                        table.add_column("Waypoints", style="yellow")
                        table.add_column("Destination", style="bright_blue")
                        table.add_column("Distance", style="bright_green")
                        for r in routes:
                            wpts = r[4] if r[4] else "N/A"
                            table.add_row(str(r[0]), r[1], r[2], r[3], wpts, r[5])
                        console.print(table)
                    input("Press Enter to continue...")
                elif rchoice == "View Route":
                    clear()
                    routes = db.routes.fetch_all()
                    if not routes:
                        console.print("[yellow]No routes found to view.[/yellow]")
                        sleep(2)
                        continue
                    rid = questionary.text("Enter route ID to view:").ask()
                    if not rid or not rid.isdigit() or int(rid) < 1 or rid not in [str(r[0]) for r in routes]:
                        console.print("[red]Invalid route ID. Please try again.[/red]")
                        sleep(2)
                        continue
                    rid = int(rid)
                    try:
                        route = db.routes.fetch_route(rid)
                    except Exception as e:
                        console.print(f"[red]Error fetching route: {e}[/red]")
                        sleep(2)
                        continue
                    if not route:
                        console.print("[yellow]Route not found.[/yellow]")
                        sleep(2)
                        continue
                    r = route[0]
                    wpts = r[3] if r[3] else "N/A"
                    panel = Panel.fit(f"[bold magenta]Name:[/bold magenta] {r[1]}\n[bold green]Origin:[/bold green] {r[2]}\n[bold yellow]Destination:[/bold yellow] {r[4]}\n[bold bright_blue]Waypoints:[/bold bright_blue] {wpts}\n[bold bright_green]Distance:[/bold bright_green] {r[5]}", title=f"Route ID {r[0]} Details", border_style="cyan")
                    console.print(panel)
                    input("Press Enter to continue...")
        elif choice == "8":
            while True:
                clear()
                console.print("[bold blue]Naval Fleet Management System - Settings[/bold blue]")
                schoice = questionary.select(
                    "Settings Menu - Select an option:",
                    choices=[
                        questionary.Choice(title=[("class:blue", "Master Settings")], value="Master Settings"),
                        questionary.Choice(title=[("class:magenta", "Host Settings")], value="Host Settings"),
                        questionary.Choice(title=[("class:yellow", "About")], value="About"),
                        questionary.Choice(title=[("class:exit", "Back to Main Menu")], value="Back to Main Menu"),
                    ], style=custom_style
                ).ask()
                if schoice == "Master Settings":
                    while True:
                        clear()
                        console.print("[bold blue]Naval Fleet Management System - Master Settings[/bold blue]")
                        mchoice = questionary.select(
                            "Master Settings - Select an option:",
                            choices=[
                                questionary.Choice(title=[("class:blue", "Change Master Password")], value="Change Master Password"),
                                questionary.Choice(title=[("class:exit", "Back to Settings Menu")], value="Back to Settings Menu"),
                            ], style=custom_style).ask()
                        if mchoice == "Back to Settings Menu":
                            clear()
                            break
                        elif mchoice == "Change Master Password":
                            clear()
                            current_password = questionary.password("Enter current master password:").ask()
                            if not current_password:
                                console.print("[red]Current password cannot be empty. Please try again.[/red]")
                                sleep(2)
                                continue
                            if not master.verifypassword(current_password):
                                console.print("[red]Incorrect current password. Please try again.[/red]")
                                sleep(2)
                                continue
                            new_password = questionary.password("Enter new master password:").ask()
                            if not new_password:
                                console.print("[red]New password cannot be empty. Please try again.[/red]")
                                sleep(2)
                                continue
                            confirm_password = questionary.password("Confirm new master password:").ask()
                            if new_password != confirm_password:
                                console.print("[red]Passwords do not match. Please try again.[/red]")
                                sleep(2)
                                continue
                            master.changepassword(new_password)
                            console.print("[green]Master password changed successfully.[/green]")
                            sleep(2)
                elif schoice == "Host Settings":
                    while True:
                        clear()
                        console.print("[bold blue]Naval Fleet Management System - Host Settings[/bold blue]")
                        hchoice = questionary.select(
                            "Host Settings - Select an option:",
                            choices=[
                                questionary.Choice(title=[("class:blue", "Add Host")], value="Add Host"),
                                questionary.Choice(title=[("class:magenta", "Update Host")], value="Update Host"),
                                questionary.Choice(title=[("class:yellow", "Delete Host")], value="Delete Host"),
                                questionary.Choice(title=[("class:green", "View Host")], value="View Host"),
                                questionary.Choice(title=[("class:bright_green", "Show All Hosts")], value="Show All Hosts"),
                                questionary.Choice(title=[("class:bright_yellow", "Change Host")], value="Change Host"),
                                questionary.Choice(title=[("class:exit", "Back to Settings Menu")], value="Back to Settings Menu"),
                            ], style=custom_style
                        ).ask()
                        if hchoice == "Back to Settings Menu":
                            clear()
                            break
                        elif hchoice == "Add Host":
                            clear()
                            hostname = questionary.text("Enter host:").ask()
                            password = questionary.password("Enter host password:").ask()
                            if not all([hostname, password]):
                                console.print("[red]Host and password cannot be empty. Please try again.[/red]")
                                sleep(2)
                                continue
                            try:
                                hosts.addhost(hostname, password)
                            except Exception as e:
                                console.print(f"[red]Could not add host. Error: {e}[/red]")
                                sleep(2)
                                continue
                            console.print(f"[green]Host '{hostname}' added successfully.[/green]")
                            sleep(2)
                        elif hchoice == "Update Host":
                            clear()
                            host_list = hosts.gethosts()
                            if not host_list:
                                console.print("[yellow]No hosts found to update.[/yellow]")
                                sleep(2)
                                continue
                            hname = questionary.select(
                                "Select host to update:",
                                choices=[f"{h[1]}" for h in host_list]
                            ).ask()
                            if not hname:
                                console.print("[red]No host selected. Please try again.[/red]")
                                sleep(2)
                                continue
                            password = questionary.password("Enter new host password:").ask()
                            if not password:
                                console.print("[red]Password cannot be empty. Please try again.[/red]")
                                sleep(2)
                                continue
                            hostid = None
                            for h in host_list:
                                if h[1] == hname:
                                    hostid = h[0]
                                    break
                            hosts.updatehost(hostid, hname, password)
                            console.print(f"[green]Host '{hname}' updated successfully.[/green]")
                            sleep(2)
                        elif hchoice == "Delete Host":
                            clear()
                            host_list = hosts.gethosts()
                            if not host_list:
                                console.print("[yellow]No hosts found to delete.[/yellow]")
                                sleep(2)
                                continue
                            hname = questionary.select(
                                "Select host to delete:",
                                choices=[f"{h[1]}" for h in host_list]
                            ).ask()
                            if not hname:
                                console.print("[red]No host selected. Please try again.[/red]")
                                sleep(2)
                                continue
                            confirm = questionary.confirm(f"Are you sure you want to delete host '{hname}'?").ask()
                            if not confirm:
                                console.print("[yellow]Deletion cancelled.[/yellow]")
                                sleep(2)
                                continue
                            hostid = None
                            for h in host_list:
                                if h[1] == hname:
                                    hostid = h[0]
                                    break
                            hosts.deletehost(hostid)
                            console.print(f"[green]Host '{hname}' deleted successfully.[/green]")
                            sleep(2)
                        elif hchoice == "View Host":
                            clear()
                            host_list = hosts.gethosts()
                            if not host_list:
                                console.print("[yellow]No hosts found to view.[/yellow]")
                                sleep(2)
                                continue
                            hname = questionary.select(
                                "Select host to view:",
                                choices=[f"{h[1]}" for h in host_list]
                            ).ask()
                            if not hname:
                                console.print("[red]No host selected. Please try again.[/red]")
                                sleep(2)
                                continue
                            hostid = None
                            for h in host_list:
                                if h[1] == hname:
                                    hostid = h[0]
                                    break
                            host_details = hosts.gethost(hostid)
                            password = hosts.getpassword(hname)
                            panel = Panel.fit(f"[bold magenta]Hostname:[/bold magenta] {host_details[0][1]}\n[bold green]Password:[/bold green] {password}", title=f"Host ID {host_details[0][0]} Details", border_style="cyan")
                            console.print(panel)
                            input("Press Enter to continue...")
                        elif hchoice == "Show All Hosts":
                            clear()
                            host_list = hosts.gethosts()
                            if not host_list:
                                console.print("[yellow]No hosts found.[/yellow]")
                                sleep(2)
                                continue
                            table = Table(title="All Hosts")
                            table.add_column("Host ID", style="cyan", no_wrap=True)
                            table.add_column("Hostname", style="magenta")
                            for h in host_list:
                                table.add_row(str(h[0]), h[1])
                            console.print(table)
                            input("Press Enter to continue...")
                        elif hchoice == "Change Host":
                            clear()
                            host_list = hosts.gethosts()
                            hname = questionary.select(
                                "Select host to change to:",
                                choices=[f"{h[1]}" for h in host_list]
                            ).ask()
                            if not hname:
                                console.print("[red]No host selected. Please try again.[/red]")
                                sleep(2)
                                continue
                            password = hosts.getpassword(hname)
                            try:
                                db.changehost(hname, password)
                            except Exception as e:
                                console.print(f"Could not connect to the host.\n[red]Error: {e}[/red]")
                                sleep(2)
                                continue
                            console.print(f"[green]Switched to host '{hname}' successfully.[/green]")
                            sleep(2)
                elif schoice == "About":
                    clear()
                    console.print("[bold blue]Naval Fleet Management System - About[/bold blue]")
                    about = about_text = """
Welcome aboard!

This is a simple, secure, and menu-driven CLI application built with Python.
It helps you manage day-to-day naval operations using a MySQL database,
which can be hosted locally or in the cloud.

Main Features:
 • Crew management
 • Ship records
 • Mission planning & mission logs
 • Inventory tracking
 • Bases & route planning

Highlights:
 • Secure login with master password
 • Switch easily between local and cloud database
 • Multi-user access support
 • Organized and efficient data management

This project shows how Python and MySQL can work together in a neat,
text-based environment to keep naval operations running smoothly.
"""
                    panel = Panel.fit(about, title="Naval Fleet Management System", border_style="green")
                    console.print(panel)
                    input("Press Enter to continue...")
                elif schoice == "Back to Main Menu":
                    clear()
                    break
close()