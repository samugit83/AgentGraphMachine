
curl -X POST http://localhost:5000/agent-planner \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "3354564632526",
           "user_id": "12345678956220",
           "session_chat_history": [{
                "role": "user",
                "content": "Hi, I’ve been experiencing some symptoms recently, and I’m concerned about what they might indicate. I’ve noticed that I’m feeling extremely thirsty all the time, I have to urinate much more frequently than usual, and I’ve lost some weight without trying. I also feel very tired most of the day, even after getting enough sleep. Could you help me understand what might be causing these symptoms?"
            }
            ]
         }'



curl -X POST http://localhost:5000/agent-planner \
     -H "Content-Type: application/json" \
     -d '{                
           "session_id": "3354564632526",
           "user_id": "1234567890",
           "session_chat_history": [
             {
               "role": "user",
               "content": "no"
             }
           ]
         }'


curl -X POST http://localhost:5000/agent-planner \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "3434534542",
           "user_id": "1234567890",
           "session_chat_history": [
             {
               "role": "user",
               "content": "Hi, I’ve been experiencing some symptoms recently, and I’m concerned about what they might indicate. I’ve noticed that I’m feeling extremely thirsty all the time, I have to urinate much more frequently than usual, and I’ve lost some weight without trying. I also feel very tired most of the day, even after getting enough sleep. Could you help me understand what might be causing these symptoms?"
             },
             {
               "role": "assistant",
               "content": "When did you first notice these symptoms?"
             },
             {
               "role": "user",
               "content": "Ive been experiencing these symptoms for about 2 months now."
             },
             {
               "role": "assistant",
               "content": "Have you experienced any other symptoms besides those mentioned?"
             },
             {
               "role": "user",
               "content": "No, I havent experienced any other symptoms besides those mentioned."
             }
           ]
         }'



curl -X POST http://localhost:5000/agent-planner \
     -H "Content-Type: application/json" \
     -d '{
           "session_id": "3434534542",
           "user_id": "1234567890",
           "session_chat_history": [
             {
               "role": "user",
               "content": "Hi, I’ve been experiencing some symptoms recently, and I’m concerned about what they might indicate. I’ve noticed that I’m feeling extremely thirsty all the time, I have to urinate much more frequently than usual, and I’ve lost some weight without trying. I also feel very tired most of the day, even after getting enough sleep. Could you help me understand what might be causing these symptoms?"
             },
             {
               "role": "assistant",
               "content": "When did you first notice these symptoms?"
             },
             {
               "role": "user",
               "content": "Ive been experiencing these symptoms for about 2 months now."
             },
             {
               "role": "assistant",
               "content": "Have you experienced any other symptoms besides those mentioned?"
             },
             {
               "role": "user",
               "content": "No, I havent experienced any other symptoms besides those mentioned."
             },
             {
               "role": "assistant",
               "content": "Do you have any pre-existing medical conditions?"
             },
             {
               "role": "user",
               "content": "No, I dont have any pre-existing medical conditions."
             },
             {
               "role": "assistant",
               "content": "What is your age and gender?"
             },
             {
               "role": "user",
               "content": "I am 30 years old and male."
             },
             {
               "role": "assistant",
               "content": "Have you recently changed your diet or physical activity levels?"
             },
             {
               "role": "user",
               "content": "Yes, I have recently changed my diet and physical activity levels."
             }
           ]
         }'