document.addEventListener('DOMContentLoaded', ()=>{
    // input and send button
    const messageInputField = document.getElementById('message-input');

    const messageSendButton = document.getElementById('message-send');

    // message list area
    const messageListArea = document.getElementById('message-list-area');

    function sendMessage(){
        // add a new message
        let messageToSend = messageInputField.value;

        let currentTime = new Date();


        let hoursInTwelveFormat;

        // time
        if (currentTime.getHours() % 12 === 0){
            hoursInTwelveFormat = 12;

        } else {
            hoursInTwelveFormat = currentTime.getHours() % 12;
        }


        let currentMinutes = String(currentTime.getMinutes()).padStart(2, '0');

        let amOrPm = currentTime.getHours() >= 12 ? 'PM': 'AM';

        let currentTimeString = `${hoursInTwelveFormat}:${currentMinutes} ${amOrPm}`;
        
        // message template code
        let messageTemplate =  `
                                <div class="card">
                                    <div class="card-body bg-primary">
                                        <div class="d-flex justify-content-start">
                                            Sandryne Lyton
                                        </div>

                                        <span class="text-white">
                                            ${messageToSend}
                                        </span>

                                        <div class="d-flex justify-content-end">
                                            <span class="card-text text-muted">
                                            ${currentTimeString}
                                            </span>
                                        </div>
                                    </div>

                                </div>
        `;
        
        let newMessageBubble = document.createElement('div');

        // add bubble attributes
        newMessageBubble.classList.add('col-12');

        newMessageBubble.classList.add('d-flex');

        newMessageBubble.classList.add('justify-content-end');

        newMessageBubble.classList.add('mb-3');

        // add bubble contents
        newMessageBubble.innerHTML = messageTemplate;

        // load the message into list
        messageListArea.appendChild(newMessageBubble);

        messageInputField.value = "";
    }

    // track send
    messageSendButton.addEventListener('click', ()=>{
        if (messageInputField.value.length > 0){
            sendMessage();
        }
    });

    messageInputField.addEventListener('keydown', (pressEvent)=>{
        if (pressEvent.key === 'Enter'){
            sendMessage();
        }
    });


});