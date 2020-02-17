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

args = commandArgs(trailingOnly=TRUE)
if (length(args)<2) {
  stop("Rscript score.R [model file] <inputfile> <outputfile>.n", call.=FALSE)
} else if (length(args)<3) {
  modelfile = ''
  inputfile = args[1]
  outputfile = args[2]
} else {
  modelfile = args[1]
  inputfile = args[2]
  outputfile = args[3]
}

inputdata <- read.csv(file=inputfile, header=TRUE, sep=",")

for(i in 1:ncol(inputdata)){
  if(i!= 5 && i!=6){
    inputdata[is.na(inputdata[,i]), i] <- mean(inputdata[,i], na.rm = TRUE)
  }
}

if (modelfile == '') {
  files <- list.files(pattern = "\\.rda$")

  if(length(files) == 0) {
     print("not found rda file in the directory!")
     stop()
  }

  modelfile<-files[[1]]
}

model<-load(modelfile)

# -----------------------------------------------
# SCORE THE MODEL
# -----------------------------------------------
score<- predict(get(model), inputdata, type="vector")

P_BAD1<-score
P_BAD0<-1-P_BAD1

# -----------------------------------------------
# MERGING PREDICTED VALUE WITH MODEL INPUT VARIABLES
# -----------------------------------------------
mm_outds <- cbind(inputdata, P_BAD0, P_BAD1)

#mm_outds <- cbind(P_BAD0, P_BAD1)
write.csv(mm_outds, file = outputfile, row.names=F)

