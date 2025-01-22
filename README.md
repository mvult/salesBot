## Current Issues
- No ping on message
- No analytics
- Hard to track experiments.  There's zero ability to view experiments vs. success
- Friction in Fresh.  Lots of semantics across status.
- Existing AI chatbots bound to their initial platform.  Freddy sucks, quick replies suck.
- Salesmanship lacking 
  - Untimely responses
  - Too robotic.  Needs that warmth.
  - Not actually answering the question 
  - Lacking information
  - Skipping to the end, just making the offer without drawing them in

## Requirements
- Mobile app with functional notifications
- Human-in-the-loop AI integration
- Pathway to full controlled AI chatbots
- Good Analytics
- Chat export

## Future Fixes
- Systematic re-activation based on schedule.  Have we ever successfully reactivated anyone?
- Full AI-in-the-loop
- RAG if necessary

## Potential experiments for chatbot
- Offer wider price range including low price to entice tire kickers
- More direct question answering
- Different prices


### Other tools
- Chatwoot is an open-source potential replacement for fresh.  Also promises a more open Chatbot integration experience
- ChatScope is a UI framework for chat applications, in case we completely want to roll our own solution https://github.com/chatscope/chat-ui-kit-react?tab=readme-ov-file
- Crisp is another potential replacement for Fresh.  High probability that we can pipe custom responses here through an API. 
- Dialog Flow might do everything we want, but might also be quite limited.


### Running questions
Erika Jimenez seems like a 'bad' conversation, but it seemed to have worked.  We ignore her questions and things like that.  Is what I see in instagram/fresh accurate?  I.e., the missed questions and the repetitions?


### Streamlit Anthropic Implementation notes
https://docs.anthropic.com/en/api/messages
https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching#tracking-cache-performance
https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/customer_service_agent.ipynb



## TODO 
- Add sender and receiver ID's to message x
- test_messaging.py file x
- lay out main work Flow
  - message enters
  - if new conversation, add agent based on multi-arn
  - add message to DB
  - sets background task, passes through 'should_pass_to_LLM' function in 30 secs.  
  - If so, groups all unhandled messages into a bundled message by adding ID
  - passes bundled messages to LLM
  - receives bundled message
  - splits it into sub-messages
  - saves sub-messages, groups them by ID
