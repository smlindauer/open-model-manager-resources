# Copyright SAS Institute
#
#  Licensed under the Apache License, Version 2.0 (the License);
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

inputdata <- read.csv(file="hmeq_train.csv", header=TRUE, sep=",")

for(i in 1:ncol(inputdata)){
  if(i!= 5 && i!=6){
    inputdata[is.na(inputdata[,i]), i] <- mean(inputdata[,i], na.rm = TRUE)
  }
}

library(rpart)
# -----------------------------------------------
# FIT THE LOGISTIC MODEL
# -----------------------------------------------
dtree<- rpart(BAD ~ MORTDUE + LOAN + VALUE + factor(REASON) + factor(JOB) + DEROG + CLAGE + NINQ + DELINQ + DEBTINC, data = inputdata)

# -----------------------------------------------
# SAVE THE OUTPUT PARAMETER ESTIMATE TO LOCAL FILE OUTMODEL.RDA
# -----------------------------------------------
save(dtree, file="dtree.rda")