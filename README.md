# pmt-dashboard
A Grafana dashboard implementation offering unified observability over a suite of patch management tools. 

## API Key - Environment Variables

Tenable API keys (an access key and a secret key) are required to properly execute this program. It is recommended that you set environment variables to keep the credentials on your system. The below guidance follows recommendations from OpenAI on the best practices for API Key Safety, available [here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety).

### Windows

- **Option 1**: Set your 'TENABLE_ACCESS_KEY' and 'TENABLE_SECRET_KEY' Environment Variables via the **cmd prompt**
- Run the following in the cmd prompt, replacing \<ACCESS_KEY> and \<SECRET_KEY> with your keys, as below:

```
setx TENABLE_ACCESS_KEY "<ACCESS_KEY>"
setx TENABLE_SECRET_KEY "<SECRET_KEY>"
```
- This will not apply to the current cmd prompt window, so open a new one to use that variable
- Validate that the variable has been set by opening a cmd prompt window and typing in the following:

```
echo %TENABLE_ACCESS_KEY%
echo %TENABLE_SECRET_KEY%
```
- **Option 2**: Set your 'TENABLE_ACCESS_KEY' and 'TENABLE_SECRET_KEY' Environment Variables through the **Control Panel**
1. Open **System** properties and select **Advanced system settings**
2. Select **Environment Variables...**
3. Select **New...** from the User variables section (top)
4. Add your name/key value pair, replacing \<ACCESS_KEY> and \<SECRET_KEY> with your keys, as below:

```
Variable name: TENABLE_ACCESS_KEY
Variable value: <ACCESS_KEY>
```
```
Variable name: TENABLE_SECRET_KEY
Variable value: <SECRET_KEY>
```

### Linux/MacOS

- **Option 1**: Set your 'TENABLE_ACCESS_KEY' and 'TENABLE_SECRET_KEY' Environment Variables using **zsh**
1. Run the following command in your terminal, replacing \<ACCESS_KEY> and \<SECRET_KEY> with your keys, as below:

```
echo "export TENABLE_ACCESS_KEY='<ACCESS_KEY>'" >> ~/.zshrc
echo "export TENABLE_SECRET_KEY='<SECRET_KEY>'" >> ~/.zshrc
```
2. Update the shell with the new variables:

```
source ~/.zshrc
```
3. Confirm that you have set your environment variables using the following command:

```
echo $TENABLE_ACCESS_KEY
echo $TENABLE_SECRET_KEY
```

- **Option 2**: Set your 'TENABLE_ACCESS_KEY' and 'TENABLE_SECRET_KEY' Environment Variables using **bash**
1. Run the following command in your terminal, replacing \<ACCESS_KEY> and \<SECRET_KEY> with your keys, as below:

```
echo "export TENABLE_ACCESS_KEY='<ACCESS_KEY>'" >> ~/.bash_profile
echo "export TENABLE_SECRET_KEY='<SECRET_KEY>'" >> ~/.bash_profile
```
2. Update the shell with the new variables:

```
source ~/.zshrc
```
3. Confirm that you have set your environment variables using the following command:

```
echo $TENABLE_ACCESS_KEY
echo $TENABLE_SECRET_KEY
```