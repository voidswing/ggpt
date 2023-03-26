# ggpt

##### Gorgeous CLI tools using GPT.

<br/>
<br/>

## Installation


```
pip install ggpt
```

<br/>
<br/>

## Setup
1. Obtain an OpenAI API key at https://beta.openai.com/account/api-keys

2. Add it to your shell environment variables
	```
	export OPENAI_API_KEY=<YOUR_API_KEY_HERE>
	```

<br/>
<br/>

## Usage

<br/>

###  docstring

###### generates automated docstring based on code changes.


<br/> 

```
ggpt docstring [OPTIONS]
```

<br/>

| Option         | Description                                       |
| -------------- | ------------------------------------------------- |
| `--api-key TEXT`|OpenAI API Key. <br/> If not provided, `OPENAI_API_KEY` environment variable is used. |
| `--path PATH`   | Path to the Git repository to search for code changes. <br/> If not provided, the current directory is used.|
| `--hash TEXT`   | Hash of the commit to review. <br/>  If not provided, unstaged changes are reviewed by default.     |
| `--staged`      | Include only staged changes in the review. <br/> If not provided, unstaged changes are reviewed by default.  |

<br/>

https://user-images.githubusercontent.com/123562684/227761450-9297f709-3d61-448c-ad78-a04f9a5f41d8.mov

<br/>

---

<br/>


###  review

###### generates automated code review based on code changes.


<br/>

```
ggpt review [OPTIONS]
```

<br/>

| Option         | Description                                       |
| -------------- | ------------------------------------------------- |
| `--api-key TEXT`|OpenAI API Key. <br/> If not provided, `OPENAI_API_KEY` environment variable is used. |
| `--path PATH`   | Path to the Git repository to search for code changes. <br/> If not provided, the current directory is used.|
| `--hash TEXT`   | Hash of the commit to review. <br/>  If not provided, unstaged changes are reviewed by default.     |
| `--staged`      | Include only staged changes in the review. <br/> If not provided, unstaged changes are reviewed by default.  |

<br/>

https://user-images.githubusercontent.com/123562684/227762097-1c42b186-014f-48fe-b116-ee5e6c39f9f7.mov

<br/>

---

<br/>


###  naming

###### suggests variable names based on submitted prompt. 


<br/>

```
ggpt naming PROMPT [OPTIONS]
```

<br/>

| Option         | Description                                       |
| -------------- | ------------------------------------------------- |
| `--api-key TEXT`|OpenAI API Key. <br/> If not provided, `OPENAI_API_KEY` environment variable is used. |

<br/>

https://user-images.githubusercontent.com/123562684/227763626-d329f156-c7f6-4a46-bfee-57504882d62c.mov


<br/>

## License


MIT LISENCE