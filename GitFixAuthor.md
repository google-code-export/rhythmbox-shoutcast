
```
git filter-branch --commit-filter '
        if [ "$GIT_AUTHOR_NAME" = "axet" ];
        then
                GIT_AUTHOR_NAME="Alexey Kuznetsov";
                GIT_AUTHOR_EMAIL="<ak@axet.ru>";
                git commit-tree "$@";
        else
                git commit-tree "$@";
        fi' -- --all

```