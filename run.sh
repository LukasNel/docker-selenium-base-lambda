ROLE_ARN=arn:aws:iam::339712742700:role/lambda-ex 
ECR_REPO=339712742700.dkr.ecr.us-east-1.amazonaws.com/hello-world
ECR_IMAGE=$ECR_REPO:latest
docker build -t docker-image:test .
docker tag docker-image:test $ECR_REPO
docker push $ECR_IMAGE
FUNCTION_NAME=hello-world-$RANDOM
aws lambda create-function  --memory-size 2048 --function-name $FUNCTION_NAME  --timeout 900 --package-type Image    --region us-east-1   --code ImageUri=$ECR_IMAGE   --role $ROLE_ARN
sleep 60
echo "Invoking the function"
aws lambda invoke  --function-name $FUNCTION_NAME --region us-east-1 response.json