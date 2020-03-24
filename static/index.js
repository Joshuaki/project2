document.addEventListener('DOMContentLoaded', () => {

               
    document.querySelector('#Name').onsubmit = () => {
        
        document.querySelector('#result').innerHTML = "This is a Test";
        // Initialize a new request
        const request = new XMLHttpRequest();
        const username = document.querySelector('#username').value
        request.open('POST', '/register');
        
        // Callback function for when request completes
        request.onload = () => {

            // Extract JSON data from request
            const data = JSON.parse(request.responseText);
            
            document.querySelector('#result').innerHTML = data.users;
            //document.querySelector('#result').innerHTML = `Welcome ${data}`;
            
        }


        //add data to send with request
        const data = new FormData();
        data.append('username', username)

        //send request
        request.send(data);
        return false;
    };

});