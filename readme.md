![alt tag](https://raw.githubusercontent.com/erfan111/newsEngine/master/resources/logo.png)

### NewsEngine Project Report



Advanced Information Retrieval Course

Group Members:

Seyyed Alireza Sanaee

Erfan Sharafzadeh

Mahdi Bagvand

Hooman Behnejad





Iran University of Science and Technology



Bahman 1395

Check out [newsEngineCrawler](https://github.com/erfan111/newsEngineCrawler)  
Check out [newsEngine](https://github.com/erfan111/newsEngine)  

--------------

1. ##Project Description

    - The aim of the project was to design and implement a web based News article crawler and also implement a Search Engine for indexing and retrieval of data.

2. ##Requirements

    - News Article Crawler which supports Farsi Press websites
    
    - Near Duplicate and Similar Article finder
    
    - Document Indexing System
    
    - Article Retrieval System
    
3. ##Project Overview

As depicted below, the project is consisted of 4 major subsystems which interact with each other asynchronously.

![alt tag](https://raw.githubusercontent.com/erfan111/newsEngine/master/resources/integration.png)

3.1. System Function Scenario

Crawler is started and retrieves news articles from provided root URLs. These articles are filtered based on the contents using an XPath query which specifies where the required information is located on the web page and stored in a shared repository.

We used MongoDB for our shared repository. Mongo is a Document-based database which enhanced load and store overhead in comparison to traditional relational databases.

Furthermore, Each News is a document, so we don&#39;t need to do any serialization or de-serialization in the process of storing or retrieving them.

The Near Duplicate detection engine works asynchronously. It is invoked at certain times when new articles are fetched and compares each article to all available docs in database.

The indexer is invoked by crawler to construct an updated inverted index. The index is connected to a web service API which provides RESTful service to clients.

An Android application is developed to provide these services to user by leveraging the API.

3.2. Component Diagram

![alt tag](https://raw.githubusercontent.com/erfan111/newsEngine/master/resources/arch.jpg)

The diagram above shows our system's components and their relations.

As we can see, this is a shared repository architecture. The main advantage of it is the fact that the communication of the components are minimized and is relied on a centralized repository.

The repository can be replicated to avoid single point of failure.

##Components Description

3.1. Crawler

Crawler is powered by Python's Scrapy Framework and is connected to MongoDB Using MongoEngine [ORM engine].

Our crawler works in the following steps:

First crawler engine must schedule URL fetches and pipelines. In this crawler, we have to define spiders which scrap contents from the web page and generates items and new requests. Items will pass through the pipelines after they adapts from the web and if spider face the URL which must fetch at next time, it will generate a new request and pass it to crawler scheduler.

Scrapy is a python package which we choose for our crawler engine, have a scheduler. This part of the system defines and applies the policy to requests queue. Spiders emit the request and scheduler put them in the correct position in the queue. We choose FIFO discipline for our main requests queue.

After q request get out from the head of the queue, it will process and fetch from the web by Downloader and the content will pass to its spider. Spiders generates items and new URLs and this loop will remain forever.

We decided to generate no item in pipeline, but we put them in main database right after they retrieved from the content.

 ![alt tag](https://raw.githubusercontent.com/erfan111/newsEngine/master/resources/scraper.jpg)

3.2. Near Duplicate Detection Components

 Near Duplicate Detection Component is suppose to detect near duplicate documents and similar documents using JACCARD algorithm. Main approach to this problem is to break sentences up to 3-6 Grams and collect these n-gram into a Set. Then, we use Jaccard formula in order to calculate the similarity ratio of documents to each other. With a try and error method, we realize that the documents are more semantically similar when the similarity threshold is set to 30 to 40 percent. So if we come less than 30 percent, we will have irrelevant documents, and if we go near 90 percent we could not find any documents. Jaccard formula is (A∩B)/(A U B) so we need two set of n-grams to calculate in ratio.

We literally didn't work on time complexity of this approach so it is O(n2)
and it takes long for large databases.

3.3. Search Engine

Search engine is implemented in JAVA and uses an Inverted index data structure for indexing News articles. We used scalar Retrieval mechanism which is based on TF-IDF retrieval algorithm.

These values are precomputed after the indexing to speed up the process of answering user queries.

The data is provided by the MongoDB, and the method to start indexing is invoked using the web service and by the crawler component.

The query method is also called by web service.

Our search engine accepts weighted words search, positional inverted index is also available but phrase queries are not supported.

3.4. Web Service

We used the powerful Spring Framework for the web API. The standard we used is RESTful, so we designed standardized URLs and secured our API with Oauth1.0 This allows us to protect our web service from unauthorized accesses.

The controller of spring web framework responds to API calls. The framework uses dependency injection design pattern to provide programmers with simple integration of dependencies.

3.4.1. Web service dependencies

- Redis client
- Spring Security
- Spring Data
- Spring Boot starter
- Apache commons
- Jhazm Persian analyzer
- Spring Web

3.4.2. Web service API
```
-
## /news/<count>                Retrieve latest news
-
## /news/id/<id>                Retrieve an specific article
-
## /news/press/<press>        Retrieve articles from a press
-
## /news/category/<cat>        Retrieve a specific category of articles
-
## /query       POST → json { "qeury": "", "weights" : [] }     Search the index
```
