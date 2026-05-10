import typer
from typing import Optional
from checker import check_email, check_password
from scorer import calculate_risk

app = typer.Typer(help="breach-radar: check if your email or password has been exposed in known data breaches.")

# maps each risk level to a color for the terminal output
RISK_COLORS = {
    "SAFE":     typer.colors.GREEN,
    "LOW":      typer.colors.CYAN,
    "MEDIUM":   typer.colors.YELLOW,
    "HIGH":     typer.colors.RED,
    "CRITICAL": typer.colors.MAGENTA,
}

@app.command()
def scan(
    email: str = typer.Option(..., "--email", "-e", help="Email address to check"),
    password: Optional[str] = typer.Option(None, "--password", "-p", help="Password to check (optional). Uses k-anonymity — never sent in plain text.")
):
    # main function - takes email and optional password, runs both checks, prints results
    typer.echo("\nbreach-radar\n" + "-" * 40)

    # --- email check ---
    typer.echo(f"\nChecking email: {email}\n")
    breaches = check_email(email)

    if breaches is None:
        raise typer.Exit(code=1)

    if len(breaches) == 0:
        typer.secho("No breaches found for this email.", fg=typer.colors.GREEN)
    else:
        typer.secho(f"Found in {len(breaches)} breach(es):\n", fg=typer.colors.YELLOW)
        for breach in breaches:
            name = breach.get("Name", "Unknown")
            date = breach.get("BreachDate", "Unknown date")
            data_classes = ", ".join(breach.get("DataClasses", []))
            typer.echo(f"  - {name} ({date})")
            typer.echo(f"    Exposed: {data_classes}\n")

    # --- password check (optional, only runs if --password flag is passed) ---
    pwned_count = 0
    if password:
        typer.echo("-" * 40)
        typer.echo("\nChecking password (k-anonymity — your password is never sent)...\n")
        pwned_count = check_password(password)

        if pwned_count == -1:
            typer.echo("Could not check password — skipping.")
            pwned_count = 0
        elif pwned_count == 0:
            typer.secho("Password not found in any known leaks.", fg=typer.colors.GREEN)
        else:
            typer.secho(f"Password found {pwned_count:,} times in known leaks. Do not use this password.", fg=typer.colors.RED)

    # --- risk score ---
    typer.echo("\n" + "-" * 40)
    risk = calculate_risk(breaches, pwned_count)
    color = RISK_COLORS.get(risk["label"], typer.colors.WHITE)

    typer.echo("\nRisk Assessment\n")
    typer.secho(f"  Level:  {risk['label']}  (score: {risk['score']})", fg=color, bold=True)
    typer.echo(f"  Why:    {risk['explanation']}")
    typer.echo(f"  Action: {risk['advice']}")
    typer.echo("\n" + "-" * 40 + "\n")


if __name__ == "__main__":
    app()