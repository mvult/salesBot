
uvicorn main:app --reload --host 0.0.0.0

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

## Potential experiments for chatbot
- Offer wider price range including low price to entice tire kickers
- More direct question answering
- Different prices

### Other tools
- Chatwoot is an open-source potential replacement for fresh.  Also promises a more open Chatbot integration experience
- ChatScope is a UI framework for chat applications, in case we completely want to roll our own solution https://github.com/chatscope/chat-ui-kit-react?tab=readme-ov-file
- Crisp is another potential replacement for Fresh.  High probability that we can pipe custom responses here through an API. 
- Dialog Flow might do everything we want, but might also be quite limited.


### Streamlit Anthropic Implementation notes
https://docs.anthropic.com/en/api/messages
https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching#tracking-cache-performance
https://github.com/anthropics/anthropic-cookbook/blob/main/tool_use/customer_service_agent.ipynb

## TODO
- Systematic re-activation based on schedule.  Have we ever successfully reactivated anyone?
- Single-flow for insertion of messages into the DB.  Basically compare current string for match with existing messages.
- If non-chatbot message detected, do a handoff
  - Ability to toggle hand-off from the front-end
- Names on front-end
- Ordered and filtered conversations on front-end
- Add other agents
- Attach Calendly webhooks
- WhatsApp integration?  On-site?
- Automated outreach after long enough

## Monitoring
- We want Rodrigo to monitor the chatbot and find where the issues are
- Compare hit rate of 20-30% with humans to see how much of a 'hit' we take with the chatbot.
- Categorize fixes into Examples, Questions for the FAQ, and Directives

## Agent notes
- Why do we even have Precio, Planes, Detalles, etc. if we immediately want to ignore the question



