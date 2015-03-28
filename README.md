# bidengine
AI Bidder

Parser module: grab json and extract all low level signals

Encoder module: encodes extracted feature for machine learning consumption

Feature module: exctarct features we want to use for building model

ML Models module: build ml model for prediction CTR or CVR
 
Bid Optimizer module: supports several bidding startegy which uses model to compute optimal bid value

Bidder: flask API that serves requsest from frontend bidder
