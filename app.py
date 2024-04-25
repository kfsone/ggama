"""
Entry point for the web-based GUI. Creates an Eel application and
opens a browser point to it.
"""
import os
import time

import ggamaagent
import ggamaconfig

import eel


# Construct globally so we can reference it in on_user_send
eel.init('web')

@eel.expose
def on_user_send(question: str) -> None:
    """ handle a user question by printing the question as a 'you' chat,
        retrieve the predicted response and print that as a 'them' chat """
    eel.display_message(question, 'you')
    response = eel.agent.answer_question(question).strip()
    eel.display_message(response, 'them')

def start():
    """ run the app service """
    eel.start('chat.html', size=(600, 400))

if __name__ == '__main__':
    # Create a config bundle based on env/config file; if an arg
    # parse is needed, we would forward the args to this too.
    config = ggamaconfig.Config()

    # Construct the inference agent based on the config.
    agent = ggamaagent.Agent(config)

    # Expose that to the agent for us to find later.
    eel.agent = agent

    # Populate its knowledge base.
    # TODO: Move to the app on an onLoad or something, so that it can
    # display any load errors into the UI and cope with reloading etc.
    print("-- preparing agent")
    eel.agent.load()

    # Start the app
    print("-- starting web app")
    start()

