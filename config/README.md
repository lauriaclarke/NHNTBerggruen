# Configuration Explanation

At present, the configuration files are setup to enact conversation within the following groups:

- one group of three plants
- one group of two plants

Further details for each group and operation are below.

## Conversation Context

One plant within each group is designated as the sender. They will begin the conversation with a question which can be configured in the .yaml file (start_question). The next plant is asked to respond or ask another question from a particular perspective. 

For senders, the preprompt is in the format of "ask a question about this statement from the perspective of" [perspective]. 

For receivers, the preprompt is in the format of "respond ot this statement from the perspective of" [perspective]. 

Perspective is re-generated after every three exchanges as follows:
- a person / object perspective is selected from the perspectvieA list, this list recycles in a loop
- a subject / context perspective is selected from the perspectiveB list, this is chosen randomly

The complete result is a prepromt along the lines of:
- "ask a question about this statement from the perpspective of a river who hates humans"
- "ask a question about this statement from the perpspective of an environmental scientist trying to build a multispecies constitution"


## Conversation Groups

### Group of Three

This group includes plants / devices labelled SE1 - SE3.

The flow of conversation is: SE1 -> SE2 -> SE3 -> SE1 etc.

- SE1 begins the conversation by asking a question to SE2. It is configured to use an untrained instance of GPT-3.
- SE2 uses a fine-tuned instance of GPT-3 and responds to the question. 
- SE3 uses a file-tuned instance of GPT-3 and then responds to SE2, addressing its response to SE1


### Group of Two

This group includes plants / devices labelled SE4 and SE5.

The flow of conversation is between the two.

- SE4 begins the conversation by asking a question of SE5. It uses plain GPT-3.
- SE5 then answers using the fine-tuned model.
