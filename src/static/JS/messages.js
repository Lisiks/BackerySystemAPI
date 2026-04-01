export function createMessage(title, content) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message-bg');

    const messageBody = document.createElement('div');
    
    const messageTitle = document.createElement('h2');
    messageTitle.textContent = title;

    const messageContent = document.createElement('p');
    messageContent.textContent = content;

    messageBody.append(messageTitle);
    messageBody.append(messageContent);
    messageElement.append(messageBody);

    document.body.prepend(messageElement);
    messageElement.addEventListener('click', (event) => {
        if (event.target === messageElement) {
            messageElement.remove();
        }
    });

        
}
