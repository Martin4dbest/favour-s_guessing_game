import random

from flask import Flask, render_template, request, session


app = Flask(__name__)

app.secret_key = "number-guessing-game-secret-key"


def start_game():
    session["number"] = random.randint(1, 100)
    session["attempts"] = 0
    session["game_over"] = False
    session["message"] = ""
    session["message_type"] = ""


@app.route("/", methods=["GET", "POST"])
def play_game():

    # Start a new game when the player first opens the page
    if "number" not in session:
        start_game()

    message = ""
    message_type = ""

    if request.method == "POST":

        # New game button
        if request.form.get("action") == "new_game":
            start_game()

            return render_template(
                "index.html",
                attempts=0,
                message="",
                message_type="",
                game_over=False
            )

        # Don't allow guesses after winning
        if session["game_over"]:
            return render_template(
                "index.html",
                attempts=session["attempts"],
                message="This game is already finished.",
                message_type="success",
                game_over=True
            )

        # Get the guess from the frontend
        guess_text = request.form.get("guess", "").strip()

        # Check if something was entered
        if not guess_text:

            message = "Please enter a number."
            message_type = "error"

        else:

            try:
                guess = int(guess_text)

                # Make sure the number is between 1 and 100
                if guess < 1 or guess > 100:

                    message = "Please enter a number between 1 and 100."
                    message_type = "error"

                else:

                    # Count the attempt
                    session["attempts"] += 1

                    number = session["number"]

                    # Guess is too low
                    if guess < number:

                        message = "Too low! Try again."
                        message_type = "low"

                    # Guess is too high
                    elif guess > number:

                        message = "Too high! Try again."
                        message_type = "high"

                    # Correct guess
                    else:

                        message = (
                            f"Congratulations! You guessed "
                            f"the number {number} in "
                            f"{session['attempts']} attempts."
                        )

                        message_type = "success"

                        session["game_over"] = True

            except ValueError:

                message = "Please enter a valid number."
                message_type = "error"

    session["message"] = message
    session["message_type"] = message_type

    return render_template(
        "index.html",
        attempts=session["attempts"],
        message=message,
        message_type=message_type,
        game_over=session["game_over"]
    )


if __name__ == "__main__":
    app.run(debug=True)