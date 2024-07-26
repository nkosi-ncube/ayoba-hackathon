
document.addEventListener('DOMContentLoaded', () => {
    // Show default section
    showSection('chat-section');
    
    // Call the functions to fetch and display data
    fetchBusinessProfile();
    fetchAndDisplayProducts();
    fetchAndDisplayOrders();
    fetchAndDisplayInvoices();
    fetchAndDisplayPayments();
    fetchAndDisplayCustomers(); // Uncomment if you want to display customers as well
});
async function makeRequest(url, method, data) {
    const response = await fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    const result = await response.json();
    document.getElementById('result').innerText = JSON.stringify(result, null, 2);
}

async function fetchCustomers() {
    try {
        console.log("Fetching Customers .......")
        const response = await fetch('https://gatewayapi-e65e2b5c01f7.herokuapp.com/api/customers/');
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const customers = await response.json();
        console.log("Customers: " , customers)
        return customers; // Return the full customer data
    } catch (error) {
        document.getElementById('broadcast-result').innerText = `Error: ${error.message}`;
        return [];
    }
}

async function broadcastMessage() {
    const message = document.getElementById('message').value;
    if (!message) {
        document.getElementById('broadcast-result').innerText = 'Message cannot be empty!';
        return;
    }

    try {
        const customers = await fetchCustomers();
        if (customers.length === 0) {
            document.getElementById('broadcast-result').innerText = 'No customers found!';
            return;
        }

        const response = await fetch('https://gatewayapi-e65e2b5c01f7.herokuapp.com/api/messages/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                phoneNumbers: customers,
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        document.getElementById('broadcast-result').innerText = 'Message sent successfully!';
    } catch (error) {
        document.getElementById('broadcast-result').innerText = `Error: ${error.message}`;
    }
}

async function handleGetRequest(endpoint) {
    try {
        const response = await fetch(`https://gatewayapi-e65e2b5c01f7.herokuapp.com/api/${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const result = await response.json();
        console.log("Response", response);
        console.log("Result", result);
        return result; // Return the result for further processing
    } catch (error) {
       console.log("Error", error);
        return []; // Return an empty array in case of an error
    }
}

function handleFormSubmit(event, endpoint) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());
    makeRequest(`https://gatewayapi-e65e2b5c01f7.herokuapp.com/api/${endpoint}`, 'POST', data);
}

async function sendQueryToAI() {
    const query = document.getElementById('query').value;
    try {
        const response = await fetch('https://gatewayapi-e65e2b5c01f7.herokuapp.com/customer-assistance/queries/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });
        const result = await response.json();
        // document.getElementById('ai-response').innerText = JSON.stringify(result, null, 2);
        const chatBox = document.querySelector('#query-box');
        chatBox.innerHTML += `<div class="chat-message user">${query}</div>`;
        chatBox.innerHTML += `<div class="chat-message bot">${result.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (error) {
        document.getElementById('ai-response').innerText = `Error: ${error.message}`;
    }
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = section.id === sectionId ? 'block' : 'none';
    });
}

async function sendMessage(event) {
    event.preventDefault();
    const message = document.querySelector('#chat-message').value;
    const chatBox = document.querySelector('#chat-box');
    chatBox.innerHTML += `<div class="chat-message user">${message}</div>`;
    document.querySelector('#chat-message').value = '';
    
    try {
        const response = await fetch('https://gatewayapi-e65e2b5c01f7.herokuapp.com/api/messages/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                msisdns: ["+27648917936"], // Ensure this is properly formatted
                message_type: 'text',
                message_text: message
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log("Response", result);

        // Handle the response
        let response_message = fetchMessages();

        console.log("Response message", response_message);

        setTimeout(() => {
            chatBox.innerHTML += `<div class="chat-message bot">${response_message}</div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        }, 2000);
    } catch (error) {
        console.error("Error", error);
    }
}

async function fetchMessages() {
    try {
        const response = await fetch('https://gatewayapi-e65e2b5c01f7.herokuapp.com/api/messages/', {
            method: 'GET',
          
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();

        if (result.length > 0) {
            const messages = result;
            console.log("Messages", messages);
            return messages[messages.length - 1].message;
        } else {
            return "No messages found";
        }
    } catch (error) {
        console.error("Error fetching messages:", error);
        return "Error fetching messages";
    }
}

async function toggleSettings() {
    const settingsPanel = document.querySelector('#settings-panel');
    settingsPanel.classList.toggle('active');

    if (settingsPanel.classList.contains('active')) {
        const customers = await fetchCustomers();
        const customerList = document.createElement('ul');

        customers.forEach(customer => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<strong>${customer.name}</strong> - Language: ${customer.language}`;
            customerList.appendChild(listItem);
        });

        // Clear existing content and add the new customer list
        settingsPanel.innerHTML = '<h2>Settings</h2><button onclick="toggleSettings()">Close</button>';
        settingsPanel.appendChild(customerList);
    }
}


async function fetchBusinessProfile() {
    try {
        const response = await fetch('https://gatewayapi-e65e2b5c01f7.herokuapp.com/api/businessprofiles/?business_name=Ayoba Business');
        const result = await response.json();
        if (result.length > 0) {
            const profile = result[0];
            document.getElementById('profile-name').innerText = profile.business_name;
            document.getElementById('profile-description').innerText = profile.description || 'No description available';
            document.getElementById('profile-email').innerText = profile.contact_email || 'No contact email';
            document.getElementById('profile-phone').innerText = profile.contact_phone || 'No contact phone';
            document.getElementById('profile-address').innerText = profile.address || 'No address available';
            document.getElementById('profile-hours').innerText = profile.working_hours || 'No working hours information';
            document.getElementById('profile-logo').src = profile.logo || 'default-logo.png';
        } else {
            document.getElementById('profile-name').innerText = 'Profile not found';
            document.getElementById('profile-description').innerText = '';
            document.getElementById('profile-email').innerText = '';
            document.getElementById('profile-phone').innerText = '';
            document.getElementById('profile-address').innerText = '';
            document.getElementById('profile-hours').innerText = '';
            document.getElementById('profile-logo').src = 'default-logo.png';
        }
    } catch (error) {
        document.getElementById('profile-name').innerText = 'Error fetching profile';
        document.getElementById('profile-description').innerText = '';
        document.getElementById('profile-email').innerText = '';
        document.getElementById('profile-phone').innerText = '';
        document.getElementById('profile-address').innerText = '';
        document.getElementById('profile-hours').innerText = '';
        document.getElementById('profile-logo').src = 'default-logo.png';
    }
}

async function fetchAndDisplayCustomers() {
    const customers = await handleGetRequest('customers');
    const customersSection = document.getElementById('customers-section');
    const customersList = document.createElement('ul');
    customersList.className = 'list-group';

    customers.forEach(customer => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
            <h5>${customer.name}</h5>
            <p>Language: ${customer.language}</p>
        `;
        customersList.appendChild(listItem);
    });

    customersSection.appendChild(customersList);
}

async function fetchAndDisplayOrders() {
    const orders = await handleGetRequest('orders');
    const ordersSection = document.getElementById('orders-section');
    ordersSection.innerHTML = ''; // Clear any existing content

    orders.forEach(order => {
        const card = document.createElement('div');
        card.className = 'card mb-3';

        const cardBody = document.createElement('div');
        cardBody.className = 'card-body';

        const orderId = document.createElement('h5');
        orderId.className = 'card-title';
        orderId.textContent = `Order ID: ${order.id}`;

        const orderTotal = document.createElement('p');
        orderTotal.className = 'card-text';
        orderTotal.textContent = `Total: R${order.total}`;

        const orderCustomer = document.createElement('p');
        orderCustomer.className = 'card-text';
        orderCustomer.textContent = `Customer ID: ${order.customer}`;

        const orderTimestamp = document.createElement('p');
        orderTimestamp.className = 'card-text';
        orderTimestamp.textContent = `Created At: ${new Date(order.created_at).toLocaleString()}`;

        const itemList = document.createElement('ul');
        itemList.className = 'list-group list-group-flush';

        order.items.forEach(item => {
            const itemElement = document.createElement('li');
            itemElement.className = 'list-group-item';
            itemElement.innerHTML = `
                <strong>Product ID:</strong> ${item.product}<br>
                <strong>Quantity:</strong> ${item.quantity}<br>
                <strong>Price:</strong> R${item.price}
            `;
            itemList.appendChild(itemElement);
        });

        cardBody.appendChild(orderId);
        cardBody.appendChild(orderTotal);
        cardBody.appendChild(orderCustomer);
        cardBody.appendChild(orderTimestamp);
        card.appendChild(cardBody);
        card.appendChild(itemList);

        ordersSection.appendChild(card);
    });
}


async function fetchAndDisplayProducts() {
    console.log('Fetching products...'); // Log to check if function is triggered
    const products = await handleGetRequest('products');
    console.log('Products fetched:', products); // Log the fetched products

    const productsSection = document.getElementById('products-section');
    const productsList = document.createElement('ul');
    productsList.className = 'list-group';

    products.forEach(product => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
            <div class="product-item">
                <img  src="${product.image_url}" alt="${product.name}" class="product-image">
                <div class="product-details">
                    <h5>${product.name}</h5>
                    <p>Price: R${product.price}</p>
                </div>
                <button class="btn btn-primary add-to-cart" onclick="addToCart(${product.id})">
                    <i class="fa fa-shopping-cart"></i> Add to Cart
                </button>
            </div>
        `;
        productsList.appendChild(listItem);
    });

    productsSection.appendChild(productsList);
}

// Function to handle Add to Cart action
function addToCart(productId) {
    console.log(`Product ${productId} added to cart`);
    // Implement your Add to Cart logic here
}

async function fetchAndDisplayInvoices() {
    const invoices = await handleGetRequest('invoices');
    const invoicesSection = document.getElementById('invoices-section');
    const invoicesList = document.createElement('ul');
    invoicesList.className = 'list-group';

    invoices.forEach(invoice => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
            <h5>Invoice ID: ${invoice.id}</h5>
            <p>Order ID: ${invoice.order}</p>
            <p>Status: ${invoice.status}</p>
            <p>Payment ID: ${invoice.payment || 'N/A'}</p>
        `;
        invoicesList.appendChild(listItem);
    });

    invoicesSection.appendChild(invoicesList);
}

async function fetchAndDisplayPayments() {
    const payments = await handleGetRequest('payments');
    const paymentsSection = document.getElementById('payments-section');
    const paymentsList = document.createElement('ul');
    paymentsList.className = 'list-group';

    payments.forEach(payment => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
            <h5>Payment ID: ${payment.id}</h5>
            <p>Invoice ID: ${payment.invoice}</p>
            <p>Status: ${payment.status}</p>
            <p>Amount: R${payment.amount}</p>
        `;
        paymentsList.appendChild(listItem);
    });

    paymentsSection.appendChild(paymentsList);
}

async function fetchAndDisplayQueries() {
    const queries = await handleGetRequest('queries');
    const queriesSection = document.getElementById('queries-section');
    const queriesList = document.createElement('ul');
    queriesList.className = 'list-group';

    queries.forEach(query => {
        const listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
            <h5>Query ID: ${query.id}</h5>
            <p>Message: ${query.message}</p>
        `;
        queriesList.appendChild(listItem);
    });

    queriesSection.appendChild(queriesList);
}
