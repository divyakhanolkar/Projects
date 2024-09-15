library(apollo)
library(tidyverse)
library(texreg)

database <- read.csv(file = 'Subject3.csv', header = TRUE)

# Question 1 ---------------------------------------------------------------

apollo_initialise()
apollo_control=list(modelName  ="M2",
                    modelDescr ="Model to Predict Pedestrian choices: Constants Only",
                    indivID    ="InvID")

apollo_beta=c( 
              asc_left_acc      = 0,
              asc_right_acc     = 0,
              asc_centre_acc    = 0,
              asc_left_dec      = 0,
              asc_right_dec     = 0,
              asc_centre_dec    = 0,
              asc_left_const    = 0,
              asc_right_const   = 0
              )

apollo_fixed = NULL

#check if you have defined everything necessary 
apollo_inputs = apollo_validateInputs()

apollo_probabilities = function(apollo_beta, apollo_inputs, functionality="estimate"){
  
  apollo_attach(apollo_beta, apollo_inputs)			 ### Attach inputs and detach after
  on.exit(apollo_detach(apollo_beta, apollo_inputs))		 ### function exit		
  
  P = list()								 ### Create list of probabilities P
  V = list()								 ### List of utilities
  
  V[["left_acc"]]     =     asc_left_acc                   
  V[["right_acc"]]    =     asc_right_acc                      
  V[["centre_acc"]]   =     asc_centre_acc                     
  V[["left_dec"]]     =     asc_left_dec                       
  V[["right_dec"]]    =     asc_right_dec                      
  V[["centre_dec"]]   =     asc_centre_dec                     
  V[["left_const"]]   =     asc_left_const                     
  V[["right_const"]]  =     asc_right_const                   
  V[["centre_const"]] =     0                  
  
  mnl_settings = list(						       ### Define settings for model 
    
    alternatives = c(left_acc = 1, right_acc = 2, centre_acc = 3, left_dec = 7, right_dec = 8, centre_dec = 9, 
                     left_const = 4,  right_const = 5,  centre_const = 6),					 ### component	
    
    avail        = list(left_acc = 1, right_acc = 1, centre_acc = 1, left_dec = 1, right_dec = 1, centre_dec = 1, 
                        left_const = 1, right_const = 1, centre_const = 1),
    
    choiceVar    = Choice,
    
    V            = V)
  
  P[["model"]] = apollo_mnl(mnl_settings, functionality)	 ### Compute probabilities using model
  
  #P = apollo_panelProd(P, apollo_inputs, functionality)	 ### Take product across observation
  ### for same obs
  
  P = apollo_prepareProb(P, apollo_inputs, functionality)	 ### Prepare and return outputs of function
  
  return(P)
}

M2 = apollo_estimate(apollo_beta,
                     apollo_fixed,
                     apollo_probabilities,
                     apollo_inputs)

apollo_modelOutput(M2)

forecast <- apollo_prediction(M2, apollo_probabilities, apollo_inputs)