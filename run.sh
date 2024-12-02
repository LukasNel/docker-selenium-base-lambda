docker build -t docker-image:test .
docker tag docker-image:test 339712742700.dkr.ecr.us-east-1.amazonaws.com/hello-world
docker push 339712742700.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest
FUNCTION_NAME=hello-world-$RANDOM
aws lambda create-function   --function-name $FUNCTION_NAME  --timeout 900 --package-type Image    --region us-east-1   --code ImageUri=339712742700.dkr.ecr.us-east-1.amazonaws.com/hello-world:latest   --role arn:aws:iam::339712742700:role/lambda-ex 
sleep 30
aws lambda invoke  --function-name $FUNCTION_NAME --region us-east-1 response.json