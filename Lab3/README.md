# Lab 3

## Team Members
- Jiwen Li
- Cynthia Liu

## Lab Question Answers

### Question 1: Why are RESTful APIs scalable?

They are stateless, which means every request contains all the information needed to process it, so requests can be handled independently by any server...
Scalable...
Flexible...


### Question 2: According to the definition of "resources" provided in the AWS article above, What are the resources the mail server is providing to clients?

The mail entries (messages sent) are the resources that the mail server is providing.


### Question 3: What is one common REST Method not used in our mail server? How could we extend our mail server to use this method?

PUT was not used in our mail server. To use this method, we could add the option for users to edit the mail messages after they are sent, even though normal mail services don't typically offer this option.


### Question 4: Why are API keys used for many RESTful APIs? What purpose do they serve? Make sure to cite any online resources you use to answer this question!

They improve security by limiting public access of the API. Likewise, they also allow rate limiting in the same way.
