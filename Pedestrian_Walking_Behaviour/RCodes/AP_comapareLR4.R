library(apollo)
library(tidyverse)
library(texreg)

database <- read.csv(file = 'Subject3.csv', header = TRUE)

# Question 1: DCM for Predicting Pedestrain Choices ----------------------------

apollo_initialise()
apollo_control=list(modelName  ="M1",
                    modelDescr ="Multinomial Logit Model (Restricted-completely)",
                    indivID    ="InvID")

apollo_beta=c( ##Betas
  
  b_car_dist        = 0,
  b_dir             = 0,
  b_angle           = 0, 
  b_acc             = 0,
  b_dec             = 0,
  b_const           = 0,
  b_car_vel         = 0,
  b_prevChoice      = 0,
  
  ##Alternative specific constants
  
  asc_right_acc     = 0,
  asc_centre_acc    = 0,
  asc_left_dec      = 0,
  asc_right_dec     = 0,
  asc_centre_dec    = 0,
  asc_left_const    = 0,
  asc_right_const   = 0,
  asc_left_acc      = 0
)

apollo_fixed = c("b_const")

#check if you have defined everything necessary 
apollo_inputs = apollo_validateInputs()

apollo_probabilities = function(apollo_beta, apollo_inputs, functionality="estimate"){
  
  apollo_attach(apollo_beta, apollo_inputs)			 ### Attach inputs and detach after
  on.exit(apollo_detach(apollo_beta, apollo_inputs))		 ### function exit		
  
  P = list()								 ### Create list of probabilities P
  V = list()								 ### List of utilities
  
  V[["left_acc"]]	    =	asc_left_acc     + b_dir*dest_dist_left_acc	      +	b_acc*Velocity_gradient     +	b_car_dist*car_dist_left_acc	     + b_angle*Angle_Left_Acc      + b_prevChoice*PrevChoice_1 + b_car_vel*v_Vehicle_Effect
  V[["right_acc"]]	  =	asc_right_acc	   + b_dir*dest_dist_right_acc      +	b_acc*Velocity_gradient     +	b_car_dist*car_dist_right_acc	     + b_angle*Angle_Right_Acc     + b_prevChoice*PrevChoice_2 + b_car_vel*v_Vehicle_Effect
  V[["centre_acc"]]	  =	asc_centre_acc	 + b_dir*dest_dist_central_acc	  +	b_acc*Velocity_gradient     +	b_car_dist*car_dist_central_acc    + b_angle*Angle_Central_Acc   + b_prevChoice*PrevChoice_3 + b_car_vel*v_Vehicle_Effect
  V[["left_dec"]] 	  =	asc_left_dec	   + b_dir*dest_dist_left_dec	      +	b_dec*Velocity_gradient     +	b_car_dist*car_dist_left_dec	     + b_angle*Angle_Left_Dec      + b_prevChoice*PrevChoice_7 + b_car_vel*v_Vehicle_Effect
  V[["right_dec"]]	  =	asc_right_dec	   + b_dir*dest_dist_right_dec      +	b_dec*Velocity_gradient     +	b_car_dist*car_dist_right_dec	     + b_angle*Angle_Right_Dec     + b_prevChoice*PrevChoice_8 + b_car_vel*v_Vehicle_Effect
  V[["centre_dec"]]	  =	asc_centre_dec	 + b_dir*dest_dist_central_dec	  +	b_dec*Velocity_gradient     + b_car_dist*car_dist_central_dec    + b_angle*Angle_Central_Dec   + b_prevChoice*PrevChoice_9 + b_car_vel*v_Vehicle_Effect
  V[["left_const"]]	  =	asc_left_const	 + b_dir*dest_dist_left_const     +	b_const*Velocity_gradient   +	b_car_dist*car_dist_left_const	   + b_angle*Angle_Left_Const    + b_prevChoice*PrevChoice_4 + b_car_vel*v_Vehicle_Effect
  V[["right_const"]]	=	asc_right_const	 + b_dir*dest_dist_right_const	  +	b_const*Velocity_gradient	  +	b_car_dist*car_dist_right_const    + b_angle*Angle_Right_Const   + b_prevChoice*PrevChoice_5 + b_car_vel*v_Vehicle_Effect
  V[["centre_const"]]	=	                   b_dir*dest_dist_central_const	+	b_const*Velocity_gradient   +	b_car_dist*car_dist_central_const  + b_angle*Angle_Central_Const + b_prevChoice*PrevChoice_6 
  
  mnl_settings = list(						       ### Define settings for model 
    
    alternatives = c(left_acc = 1, right_acc = 2, centre_acc = 3, left_dec = 7, right_dec = 8, centre_dec = 9, 
                     left_const = 4,  right_const = 5,  centre_const = 6),					 ### component	
    avail        = list(left_acc = 1, right_acc = 1, centre_acc = 1, left_dec = 1, right_dec = 1, centre_dec = 1, 
                        left_const = 1, right_const = 1, centre_const = 1),
    choiceVar    = Choice,
    V            = V)
  
  P[["model"]] = apollo_mnl(mnl_settings, functionality)	 ### Compute probabilities using model
  
  P = apollo_prepareProb(P, apollo_inputs, functionality)	 ### Prepare and return outputs of function
  
  return(P)
}

M1 = apollo_estimate(apollo_beta,
                     apollo_fixed,
                     apollo_probabilities,
                     apollo_inputs)
apollo_modelOutput(M1) 

#Model 5 -----------------------------------------------------------------

apollo_control=list(modelName  ="M5",
                    modelDescr ="M4 minus previous choice",
                    indivID    ="InvID")

apollo_beta=c( ##Betas
  
  b_car_dist        = 0,
  b_dir             = 0,
  b_car_vel         = 0,
  
  ##Alternative specific constants
  
  asc_right_acc     = 0,
  asc_centre_acc    = 0,
  asc_left_dec      = 0,
  asc_right_dec     = 0,
  asc_centre_dec    = 0,
  asc_left_const    = 0,
  asc_right_const   = 0,
  asc_left_acc      = 0
)

apollo_fixed = NULL

#check if you have defined everything necessary 
apollo_inputs = apollo_validateInputs()

apollo_probabilities = function(apollo_beta, apollo_inputs, functionality="estimate"){
  
  apollo_attach(apollo_beta, apollo_inputs)			 ### Attach inputs and detach after
  on.exit(apollo_detach(apollo_beta, apollo_inputs))		 ### function exit		
  
  P = list()								 ### Create list of probabilities P
  V = list()								 ### List of utilities
  
  V[["left_acc"]]	    =	asc_left_acc     + b_dir*dest_dist_left_acc	      +	b_car_dist*car_dist_left_acc	   + b_car_vel*v_Vehicle_Effect
  V[["right_acc"]]	  =	asc_right_acc	   + b_dir*dest_dist_right_acc      +	b_car_dist*car_dist_right_acc	   + b_car_vel*v_Vehicle_Effect
  V[["centre_acc"]]	  =	asc_centre_acc	 + b_dir*dest_dist_central_acc	  +	b_car_dist*car_dist_central_acc  + b_car_vel*v_Vehicle_Effect
  V[["left_dec"]] 	  =	asc_left_dec	   + b_dir*dest_dist_left_dec	      +	b_car_dist*car_dist_left_dec	   + b_car_vel*v_Vehicle_Effect
  V[["right_dec"]]	  =	asc_right_dec	   + b_dir*dest_dist_right_dec      +	b_car_dist*car_dist_right_dec	   + b_car_vel*v_Vehicle_Effect
  V[["centre_dec"]]	  =	asc_centre_dec	 + b_dir*dest_dist_central_dec	  + b_car_dist*car_dist_central_dec  + b_car_vel*v_Vehicle_Effect
  V[["left_const"]]	  =	asc_left_const	 + b_dir*dest_dist_left_const     +	b_car_dist*car_dist_left_const	 + b_car_vel*v_Vehicle_Effect
  V[["right_const"]]	=	asc_right_const	 + b_dir*dest_dist_right_const	  +	b_car_dist*car_dist_right_const  + b_car_vel*v_Vehicle_Effect
  V[["centre_const"]]	=	                   b_dir*dest_dist_central_const	+	b_car_dist*car_dist_central_const  
  
  mnl_settings = list(						       ### Define settings for model 
    
    alternatives = c(left_acc = 1, right_acc = 2, centre_acc = 3, left_dec = 7, right_dec = 8, centre_dec = 9, 
                     left_const = 4,  right_const = 5,  centre_const = 6),					 ### component	
    avail        = list(left_acc = 1, right_acc = 1, centre_acc = 1, left_dec = 1, right_dec = 1, centre_dec = 1, 
                        left_const = 1, right_const = 1, centre_const = 1),
    choiceVar    = Choice,
    V            = V)
  
  P[["model"]] = apollo_mnl(mnl_settings, functionality)	 ### Compute probabilities using model
  
  P = apollo_prepareProb(P, apollo_inputs, functionality)	 ### Prepare and return outputs of function
  
  return(P)
}

M5 = apollo_estimate(apollo_beta,
                     apollo_fixed,
                     apollo_probabilities,
                     apollo_inputs)
apollo_modelOutput( M5)

#LR Test --------------------------------------------------------------------
LR = apollo_lrTest(M1,M5)
