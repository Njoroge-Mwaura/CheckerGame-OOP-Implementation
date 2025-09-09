from match import Match


class Checkers:
    """
    Main Checkers application class implementing SOLID principles:
    - SRP: Single responsibility for application management
    - OCP: Open for extension, closed for modification
    - LSP: Liskov substitution principle
    - ISP: Interface segregation principle
    - DIP: Dependency inversion principle
    """

    def __init__(self):
        self.match = Match()  # Dependency injection - follows DIP

    def run(self) -> None:
        """Run the checkers application - follows SRP"""
        self.match.start_game()


if __name__ == "__main__":
    game = Checkers()
    game.run()
