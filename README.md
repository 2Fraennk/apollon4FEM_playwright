# apollon4FEM_playwright
![context-logo](readme/apollon.png)

# Apollon brings light in the untested dark of F.E.M. with Playwright


# package activeMq
The activeMq package helps to handle dead letter queues (DLQs) and their messages.
The contained messages could not be sent to their destination, so they are placed into the DLQ.
The activeMq package take over the message handling. A suitable operation for those messages could be:
## message handling 
### 'retry' message
A retry puts the message into the former message queue from where the message came from.
In that queue the message is processed again. That is a good step for temporary issues inside the process.
### 'delete' message
If a message could not be handled by retrying, there are reasons for that. The issue has to be solved before
a message could be handled successfully. But if there is no change to solve the issue, the message could be cleaned
by delete.
## configure properties
To set required properties you have to configure the properies inside 'properties.py'.
Set the endpoint URL and credentials.

