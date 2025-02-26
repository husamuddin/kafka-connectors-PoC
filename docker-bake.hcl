group "default" {
  targets = ["kafka-connect", "seed"]
}

target "kafka-connect" {
  context = "./lib/kafka-connect"
  dockerfile = "./Dockerfile"
  tag = "ca-kafka-poc/kafka-connect:latest"
}

target "seed" {
  context = "./lib/py-seed"
  dockerfile = "./Dockerfile"
  tag = "ca-kafka-poc/py-seed:latest"
}
