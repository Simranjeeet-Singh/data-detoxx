resource "null_resource" "clear_tmp" {

  provisioner "local-exec" {
    command = "rm -r ${path.module}/../tmp/*; mkdir -p ${path.module}/../tmp/utils/python"   
  }

  triggers = {
  always_run = timestamp()
  }

}

resource "null_resource" "install_dependencies" {
  depends_on = [null_resource.clear_tmp]
  provisioner "local-exec" {
    command = "pip install -r ${path.module}/../src/lambda_one/lambda_requirements.txt -t ${path.module}/../tmp/dependencies/python"
  }
  triggers = {
  always_run = timestamp()
  }

}

resource "null_resource" "move_utils_to_tmp" {
  depends_on = [null_resource.clear_tmp]
  provisioner "local-exec" {
    command = "cp -r ${path.module}/../src/utils ${path.module}/../tmp/utils/python"
  }

  triggers = {
  always_run = timestamp()
  }

}

data "archive_file" "lambda_utils_zip" {
  depends_on = [null_resource.clear_tmp, null_resource.move_utils_to_tmp]
  excludes   = [
    "__pycache__"  // Adjusted pattern to properly exclude __pycache__ directories
  ]
  type             = "zip"
  source_dir      = "${path.module}/../tmp/utils"
  output_path      = "${path.module}/../tmp/lambda_utils.zip"
}

data "archive_file" "lambda_one_dependencies_zip" {
  depends_on = [null_resource.clear_tmp, null_resource.install_dependencies]
  excludes   = [
    "/python/__pycache__"  // Doesn't work for some reason??
  ]
  type             = "zip"
  source_dir      = "${path.module}/../tmp/dependencies"
  output_path      = "${path.module}/../tmp/lambda_one_dependencies.zip"
}


data "archive_file" "lambda_one_zip" {
  excludes   = [
    "lambda_functions/__pycache__"  // Adjusted pattern to properly exclude __pycache__ directories
  ]
  depends_on = [null_resource.clear_tmp]
  type             = "zip"
  output_path      = "${path.module}/../tmp/lambda_one.zip"
  source_dir       = "${path.module}/../src/lambda_one"
}

data "archive_file" "lambda_two_zip" {
      excludes   = [
    "__pycache__"
  ]
  depends_on = [null_resource.clear_tmp]
  type             = "zip"
  output_path      = "${path.module}/../tmp/lambda_two.zip"
  source_dir       = "${path.module}/../src/lambda_two"
}