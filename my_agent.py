import argparse
from agent import Agent
from console import PygameApp
from utils import load_config


class MyAgent(Agent):

    def __init__(self):
        super(MyAgent, self).__init__()


    def reset(self):
        super(MyAgent, self).reset()


    def act(self):
        if not hasattr(self, "has_gold"):
            self.has_gold = False
        if not hasattr(self, "back_plan"):
            self.back_plan = []
        if not hasattr(self, "turn_count"):
            self.turn_count = 0
        
        if len(self.back_plan) > 0:
            action = self.back_plan.pop(0)
            self.remember_action(action)
            return action
        
        if self.last_senses is None:
            action = "FORWARD"
        elif self.last_senses["Glimmer"]:
            action = "GRAB"
        elif self.has_gold:
            action = "EXIT"
        elif self.last_senses["Bump"]:
            action = "RIGHT"
        elif self.last_senses["Breeze"] or self.last_senses["Stench"]:
            if self.turn_count % 2 == 0:
                self.back_plan = ["RIGHT", "FORWARD", "RIGHT"]
            else:
                self.back_plan = ["RIGHT", "FORWARD", "LEFT"]
            
            self.turn_count = self.turn_count + 1

            action = "RIGHT"

        else:
            action = "FORWARD"

        self.remember_action(action)
        return action
    
        return "NO_ACTION"

    def update(self, senses):
        super(MyAgent, self).update(senses)
        if not hasattr(self, "has_gold"):
            self.has_gold = False
        if not hasattr(self, "back_plan"):
            self.back_plan = []
        if not hasattr(self, "turn_count"):
            self.turn_count = 0

        if self.last_action == "GRAB" and senses["Glimmer"] == False:
            self.has_gold = True

def parse_args():
    """Read command-line options for launching the logic-agent emulator."""
    parser = argparse.ArgumentParser(description="Run Wumpus World with the logic agent.")
    parser.add_argument("--config", default="game_config.yaml", help="YAML config file for game parameters.")
    parser.add_argument("--cave", default="empty", help="Named cave profile from the YAML config.")
    parser.add_argument("--show-window", default="true", help="Override emulator.show_window from the config.")
    parser.add_argument("--seed", help="Override cave.seed from the config with an integer.")
    return parser.parse_args()


def main():
    """Create a MyAgent and launch the pygame emulator in auto-play mode."""
    args = parse_args()

    agent = MyAgent()
    config = load_config(args.config, cave_name=args.cave, show_window=args.show_window, seed=args.seed)
    PygameApp(agent=agent, config=config).run()

if __name__ == "__main__":
    main()
