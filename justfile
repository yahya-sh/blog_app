alias serve := run
alias r := run
alias s := run
alias m := migrate
alias mm := makemigrations
alias c := command
alias gl := git-log
alias gll := git-line-log


[default]
default:
    @just --list

# django runserver on 0.0.0.0:8000 (you can change the host by passing different one)
run host="0.0.0.0:8000":
    @uv run manage.py runserver {{host}}

# django migrate 
migrate app="":
    uv run manage.py migrate {{app}}

makemigrations app="":
    uv run manage.py makemigrations {{app}}

shell:
    uv run manage.py shell

collectstatic:
    uv run manage.py collectstatic --no-input

command cmd:
    uv run manage.py {{cmd}}

git-log:
    git log

git-line-log:
    git log --oneline --graph