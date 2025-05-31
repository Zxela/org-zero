from agents.director.agent import DirectorAgent

if __name__ == "__main__":
    director = DirectorAgent()
    user_msg = "Build a game to teach AI agents to kids."
    print(director.handle_user_input(user_msg))
