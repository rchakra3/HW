# DevOps HW0

## Table of Contents
  * [Git Branching Levels Code](#git-branching)
  * [Git Branching Levels](#git-branching-screenshot)
  * [Git Hooks Screencast](#git-hooks-screencast)

## Git Branching <a id="git-branching"></a>

### Introduction Sequence
#### Level 1.1

```
git commit
git commit
```

#### Level 1.2

```
git checkout -b bugFix
```

#### Level 1.3

```
git checkout -b bugFix
git commit
git checkout master
git commit
git merge bugFix
```

#### Level 1.4

```
git checkout -b bugFix
git commit
git checkout master
git commit
git checkout bugFix
git rebase master
```


### Ramping Up
#### Level 2.1

```
git checkout C4
```

#### Level 2.2

```
git checkout bugFix^
```

#### Level 2.3

```
git branch -f master C6
git branch -f bugFix C0
git checkout HEAD^
```

#### Level 2.4

```
git reset HEAD~1
git checkout pushed
git revert pushed OR git revert HEAD
```


### Moving Work Around
#### Level 3.1

```
git cherry-pick C3 C4 C7
```

#### Level 3.2

```
git rebase -i HEAD~4
```


### A Mixed Bag
#### Level 4.1

```
git checkout master
git cherry-pick C4
```

#### Level 4.2

```
git rebase -i HEAD~2
git commit --amend
git rebase -i master
git branch -f master caption
```

#### Level 4.3

```
git checkout C2
git commit --amend
git checkout master
git cherry-pick C2' C3
```

#### Level 4.4

```
git tag v0 C1
git tag v1 C2
git checkout v1
```

#### Level 4.5

```
git commit
```


### Advanced Topics
#### Level 5.1

```
git rebase side another
git rebase bugFix another
git rebase master another
git branch -f master another
```

#### Level 5.2

```
git branch bugWork~^2~
```

#### Level 5.3

```
git rebase C2 three
git rebase -i one C4
git branch -f one HEAD
git checkout two
git cherrypick C5 C4' C3' C2'
```


### Push & Pull -- Git Remotes!
#### Level 6.1

```
git clone
```

#### Level 6.2

```
git commit
git checkout o/master
git commit
```

#### Level 6.3

```
git fetch
```

#### Level 6.4

```
git pull
```

#### Level 6.5

```
git clone
git fakeTeamwork 2
git commit
git pull
```

#### Level 6.6

```
git clone
git commit
git commit
git push
```

#### Level 6.7

```
git clone
git fakeTeamwork 1
git commit
git pull --rebase
git push
```


### To Origin And Beyond -- Advanced Git Remotes!
#### Level 7.1

```
git rebase side1 side2
git rebase side2 side3
git fetch
git rebase o/master
git branch -f master side3
git push origin master
```

#### Level 7.2 [Ugh merge]

```
git checkout master
git pull
git merge side1
git merge side2
git merge side3
git push
```

#### Level 7.3 

```
git checkout -b side o/master
git commit
git pull --rebase
git push
```

#### Level 7.4

```
git push origin master
git push origin foo
```

#### Level 7.5

```
git push origin foo:master
git push origin C5:foo
```

#### Level 7.6 [3 instead of 4!]

```
git pull origin master~1:foo
git pull origin foo:master
git checkout -B foo HEAD
```

#### Level 7.7

```
git push origin :foo
git fetch origin :bar
```

#### Level 7.8

```
git pull origin bar:foo
git pull origin master:side
```


## Git Branching Screenshot <a id="git-branching-screenshot"></a>


##  Hooks Screencast <a id="git-hooks-screencast"></a>

[Link](screencast/DevOps_HW0.mp4)
