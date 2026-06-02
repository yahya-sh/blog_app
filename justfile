alias serve := run
alias r := run
alias s := run
alias m := migrate
alias mm := makemigrations
alias sm := showmigrations
alias c := command
alias log := git-log
alias llog := git-line-log
alias gllog := git-log
alias gl := git-log
alias gll := git-line-log
alias commit := git-commit
alias gcommit := git-commit
alias gc := git-commit
alias amend := git-amend
alias gamend := git-amend
alias gpush := git-push
alias gp := git-push
alias push := git-push

[default]
default:
    @just --list

# django runserver on 0.0.0.0:8000 (you can change the host by passing different one)
run host="0.0.0.0:8000":
    @uv run manage.py runserver {{host}}

# django migrate 
migrate *app="":
    uv run manage.py migrate {{app}}

makemigrations *app:
    uv run manage.py makemigrations {{app}}

showmigrations *app:
    uv run manage.py showmigrations {{app}}

shell:
    uv run manage.py shell

collectstatic:
    uv run manage.py collectstatic --no-input

command +cmd:
    uv run manage.py {{cmd}}

git-log:
    git log

git-line-log:
    git log --oneline --graph

git-commit message:
    git commit -m "{{message}}"

git-amend:
    git commit --amend

git-push remote="origin" branch="main" *args:
    git push {{remote}} {{branch}} {{args}}