## Python DNS Server
This code creates a simple DNS proxy that listens for DNS queries on port 53 and forwards the queries to Cloudflare's DNS server over TLS. When it receives a response from Cloudflare, it sends the response back to the client that made the original query. The code continuously listens for incoming queries in a loop.

---

### Code structure
The code is structured as follows:

• `create_tcp_socket()` creates a TCP socket and binds it to port 53
• `handle_query()`  handles a single DNS query from a client
• `run_proxy()` creates the TCP socket which listens for incoming connections and handles each query with the handle_query function

The `logging` module is used to create a logger, which will print messages to the console. The logger is configured to print messages of level DEBUG and above, and the format of the messages is specified.

The `log` variable is used to log messages at different levels (debug, info, warning, error, critical) depending on the situation, providing more context and visibility to the code execution.

---

### Getting the image from Docker
You can pull the image from Docker hub using the following command:

`docker pull fforfrodo/simple_proxy:latest`

---

### Configuring the DNS Server
To configure the DNS server, you will need to modify the simple_proxy.py file.

#### Bind the socket to the correct IP address:

`sock.bind(("127.0.0.1", 53))`

Replace "127.0.0.1" with the IP address of the host machine that you want to bind the socket to. This can be the external IP address of the host machine if you want to make the DNS server accessible from the internet, or the internal IP address of the host machine if you want to make the DNS server only accessible on the local network.

#### Set the destination IP address for forwarded DNS requests:

`DNS_SERVER_ADDRESS = ("1.1.1.1", 853)`
This is the IP address that the DNS server will use as the destination for forwarded DNS requests.
In this case the python DNS server forwards requests to Cloudflare over a TLS connection.

---

### Running the DNS Server
There are two ways to run the DNS server:

1. Via Python:

`sudo python3 simple_proxy.py`

This will start the DNS server with root permissions to bind it to port 53, python must already be installed locally.

2. Via Docker:

`docker build -t simple_proxy .`

`$ docker run --network=host -p 53:53 my_dns_server python3 simple_proxy.py`

This will build a Docker image based on the Dockerfile and run it in a container. The -p 53:53 flag maps the host machine's port 53 to the container's port 53, so that the DNS server will be accessible on the host machine's port 53.

---

### Testing the DNS Server

#### Check if the DNS server is running:

`ps aux | grep python`

This will list all processes running on the system that contain the word "python" in their command line. If the DNS server is running, you should see an entry for it in the list.

#### Check if the DNS server is listening on port 53:

`sudo lsof -i :53`

This will list all processes that are listening on port 53. If the DNS server is running and listening on port 53, you should see an entry for it in the list.

#### Test the DNS server by sending a request to port TCP 53 using dig:

By default, most DNS clients send requests over UDP. 
You can specify to send the request over TCP by using the "-t" option with the "dig" command:

`dig @127.0.0.1 -p 53 -t any google.com`

This will send a DNS request for the domain name google.com to the DNS server running on 127.0.0.1. 
If the DNS server is working correctly, you should see the DNS record for google.com in the output.

---

## Further considerations

### If this DNS proxy were to be deployed in an infrastructure, there are several security considerations:

1. DNS spoofing attacks: An attacker intercepts or redirects DNS queries to a malicious server, leading to man-in-the-middle attacks or phishing attempts. To mitigate this concern, you should use DNSSEC or DNS-over-TLS/HTTPS to secure the connection between the proxy and the DNS server, and configure the proxy to only accept queries from authorised sources.

2. DNS amplification attacks: The proxy could be used as an amplification vector in a DDoS attack. To mitigate this concern, you should limit the number of queries that the proxy can handle at once and implement rate limiting.

3. Access controls: Unauthorised parties could access and misuse the proxy. To mitigate this concern, you should implement access controls and authentication mechanisms, such as IP whitelisting or a username and password for accessing the proxy.

4. Insecure configurations: The proxy is not configured with secure settings, such as open ports, weak authentication or unclear access control. To mitigate this concern, you should keep the proxy software updated, and configure it with secure settings and access controls.

5. Lack of monitoring: It may be difficult to detect or respond to security incidents involving the proxy. To mitigate this concern, you should implement monitoring and logging mechanisms, such as syslog or a SIEM, to detect and respond to security incidents in a timely manner.

It's important to note that no single solution can mitigate all risks and that a comprehensive security plan that combines multiple layers of protection and regularly testing and monitoring is necessary to secure the proxy.

---

### To integrate this proxy in a distributed, microservices-oriented, and containerised architecture, the following can be considered:

1. Centralised proxy: A single DNS proxy is deployed in the infrastructure, and all services are configured to use it as their primary DNS resolver. This can be done by pointing the /etc/resolv.conf file to the IP address of the centralised proxy. This approach is simple to set up and easy to manage, but it can become a bottleneck if the proxy is not properly scaled.

2. Sidecar proxy: A DNS proxy is deployed as a sidecar container alongside each service. This can be done by creating a pod in Kubernetes that includes both the service and the sidecar proxy. This allows for better scalability and fault tolerance, as each service has its own dedicated proxy. However, it can increase the complexity of the overall system and may require additional resources.

3. Service mesh: A service mesh such as Istio or Linkerd can be used to manage the communication between services, including DNS resolution. This can be done by configuring the service mesh to route DNS queries through the proxy. This approach provides a high level of flexibility and scalability, but it can also be more complex to set up and manage.

4. Hybrid approach: A combination of the above approaches can be used to provide a balance of scalability, fault tolerance, and ease of management. For example, a centralised proxy could be used for most services, but a sidecar proxy could be used for services that require high availability or high throughput. This can be done by routing traffic to a centralised proxy but deploying a sidecar proxy for specific services that need additional scalability or fault tolerance.

In this approach, the centralised proxy would handle the majority of DNS queries, but for specific services that require high availability or high throughput, a sidecar proxy would be deployed alongside the service. This way, the sidecar proxy would handle the queries for that specific service, providing better scalability and fault tolerance for that service, while the centralised proxy would handle the queries for the other services.

It's important to note that the specific implementation details will depend on the specific architecture and technologies being used, and that a thorough testing and monitoring should be done to ensure that the proxy is functioning correctly, and that it is able to handle the expected traffic and load, and that it is able to scale as the architecture grows.

---

### Futher dvelopments:

• Caching: To improve performance and reduce the load on the destination DNS server, the DNS proxy could implement caching of DNS records. The DNS proxy could store the responses received from the destination DNS server in a cache, and use the cached responses to serve subsequent requests for the same domain name.

• Configuration: It would be useful to add a configuration system that allows the DNS proxy to be easily configured and customised without requiring code changes. This could include options such as the destination DNS server to use, the cache expiration time, and security settings.

• Testing: It would be important to add a comprehensive test suite to the DNS proxy to ensure that it is reliable and behaves as expected. This could include unit tests, integration tests, and performance tests.
