import random

from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

# Secret key is required for Flask sessions.
app.secret_key = "favour-guess-secret-key"


def start_game():
    """Start a new game and store the game information in the session."""
    session["number"] = random.randint(1, 100)
    session["attempts"] = 0
    session["game_started"] = True
    session["game_won"] = False
    session["message"] = ""
    session["message_type"] = ""


@app.route("/", methods=["GET", "POST"])
def index():
    # If the player is submitting their name
    if request.method == "POST" and "player_name" in request.form:
        player_name = request.form.get("player_name", "").strip()

        if not player_name:
            return render_template(
                "index.html",
                name_error="Please enter your name to start the game."
            )

        # Save the player's name
        session["player_name"] = player_name

        # Start a fresh game
        start_game()

        return redirect(url_for("index"))

    # If the player is submitting a guess
    if request.method == "POST" and "guess" in request.form:
        # Make sure a player has started the game
        if not session.get("game_started"):
            return redirect(url_for("index"))

        guess_text = request.form.get("guess", "").strip()

        # Validate that the guess is a number
        try:
            guess = int(guess_text)
        except ValueError:
            session["message"] = "Please enter a valid number."
            session["message_type"] = "error"

            return render_template(
                "index.html",
                player_name=session.get("player_name"),
                game_started=session.get("game_started"),
                game_won=session.get("game_won"),
                attempts=session.get("attempts", 0),
                message=session.get("message"),
                message_type=session.get("message_type"),
            )

        # Validate the number range
        if guess < 1 or guess > 100:
            session["message"] = "Please enter a number between 1 and 100."
            session["message_type"] = "error"

            return render_template(
                "index.html",
                player_name=session.get("player_name"),
                game_started=session.get("game_started"),
                game_won=session.get("game_won"),
                attempts=session.get("attempts", 0),
                message=session.get("message"),
                message_type=session.get("message_type"),
            )

        # Count the attempt
        session["attempts"] = session.get("attempts", 0) + 1

        number = session["number"]

        # Check the guess
        if guess < number:
            session["message"] = "Too low! Try again."
            session["message_type"] = "low"

        elif guess > number:
            session["message"] = "Too high! Try again."
            session["message_type"] = "high"

        else:
            session["message"] = (
                f"Congratulations, {session.get('player_name', 'Player')}!"
            )
            session["message_type"] = "success"
            session["game_won"] = True

        return redirect(url_for("index"))

    return render_template(
        "index.html",
        player_name=session.get("player_name"),
        game_started=session.get("game_started", False),
        game_won=session.get("game_won", False),
        attempts=session.get("attempts", 0),
        message=session.get("message", ""),
        message_type=session.get("message_type", ""),
        number=session.get("number"),
        name_error=None,
    )


@app.route("/new-game")
def new_game():
    """Start another game while keeping the player's name."""
    player_name = session.get("player_name")

    session.clear()

    if player_name:
        session["player_name"] = player_name
        start_game()

    return redirect(url_for("index"))


@app.route("/change-player")
def change_player():
    """Clear the current player and return to the name screen."""
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)