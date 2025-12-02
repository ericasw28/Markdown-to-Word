---
tags:
  - formatting
  - obsidian
  - mermaid
  - markdown
banner: "https://photographypro.com/wp-content/uploads/2018/01/shoot-panoramic-photos-2.jpg"
banner_y: 0.20398
---
Back 

# Contents
1. [Obsidian Formatting](#Obsidian%20Formatting)
2. [Images](#Images)
3. [Titres](#Titres)
4. [Titre 1](#Titre%201)
	1. [Titre 2](#Titre%202)
		1. [Titre 3](#Titre%203)
5. [Forme générale du texte](#Forme%20g%C3%A9n%C3%A9rale%20du%20texte)
	1. [Texte](#Texte)
	2. [Listes](#Listes)
		1. [Simple Lists](#Simple%20Lists)
		2. [Check boxes](#Check%20boxes)
6. [Tables](#Tables)
7. [Code blocks](#Code%20blocks)
8. [Mermaid Stuff](#Mermaid%20Stuff)
	1. [Entity Relationship Diagram](#Entity%20Relationship%20Diagram)
	2. [Flowchart](#Flowchart)
	3. [Sequence Diagram](#Sequence%20Diagram)
	4. [Latex Math](#Latex%20Math)
9. [State Diagrams](#State%20Diagrams)
10. [Pie Charts](#Pie%20Charts)
11. [Callouts](#Callouts)
		1. [Exemple of a code exemple in R](#Exemple%20of%20a%20code%20exemple%20in%20R)
12. [Gantt Diagrams](#Gantt%20Diagrams)


# Obsidian Formatting

Cette note contient les bases du formatting d'Obsidian

# Images

![](LogoVulcain.png) 


___
# Titres

```
# Titre 1 
## Titre 2
### Titre 3
#### Titre 4
##### Titre 5
###### Titre 6
```
# Titre 1 
## Titre 2
### Titre 3
#### Titre 4
##### Titre 5
###### Titre 6

___
# Forme générale du texte
## Texte

Normal ***Gras Italique***    **Gras**    *ITalique*    \hl{Marqueur}    ~~Strikethrough~~    `in line code`    [Link](link)    \underline{Underline}

Downpage note [^1]

[^1]: Downpage note extension

Section link
![](Expediting - Home#^Regles)




> Quote
 
---
## Listes
### Simple Lists
 - List
 - List

1. List 
2. List
	1. Embed

### Check boxes

- [ ] Tick box
- [x] Ticked box
    - [ ] Embed me please
    - [x]  Oh yeah
        - [ ] Testing
        - [x]  PLop
            - [ ] Testing
            - [x]  PLop
                - [ ] Testing
                - [x]  PLop
                    - [ ] Testing
                    - [x]  PLop
--- 

### Types of check boxes
- [ ] Unchecked 
- [x] Regular 
- [X] Checked 
- [ ] ➖ Dropped 
- [x] ▶️ Forward 
- [x] 📅 Date 
- [x] Question 
- [x] ⚗️  Half Done
- [x] ➕ Add 
- [x] 🔍 Research 
- [x] ❗ Important 
- [x] 💡 Idea 
- [x] 🧠 Brainstorm 
- [x] 👍 Pro 
- [x] 👎 Con 
- [x] 💬 Quote 
- [x] 📝 Note 
- [x] 🔖 Bookmark 
- [x] ℹ️ Information 
- [x] 📄 Paraphrase 
- [x] 📍 Location 
- [x] 📚 Example 
- [x] ✓ Answer 
- [x] 🎁 Reward 
- [x] 🔀 Choice 
- [x] ⚙️ Doing
- [x] ⏰ Time 
- [x] 👤 Character / Person
- [x] 💬 Talk
- [x] 📋 Outline / Plot 
- [x] ⚔️ Conflict 
- [x] 🌍 World 
- [x] 🔎 Clue / Find 
- [x] 🔮 Foreshadow 
- [x] ❤️ Favorite / Health 
- [x] 🔣 Symbolism 
- [x] 🤫 Secret
---
# Tables

| Table | Hey |
| ------- | ------ |
| Yay | Check|

| First name | Last name |
| ---------- | --------- |
| Max        | Planck    |
| Marie      | Curie     |
| hello      | world     |
|            |           |

---
# Code blocks
eee
~~~ 
Code block with Tildes 
~~~ 

``` 
Code Block with ticks 
``` 

    Code Block with four spaces

---
# Mermaid Stuff

## Entity Relationship Diagram
Basics of Relation design
**Note** : Relationships types disappear in read mode.
	v--> --> - - > --> <-- 
	| | - - o { 
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    ORDER ||--|{ LINE-ITEM : contains
    CUSTOMER }|..|{ DELIVERY-ADDRESS : uses
```

---
## Flowchart

This code 
	```mermaid 
	graph LR 
	A{Biology} --> Chemistry
	A -- nope --> Geology
	Chemistry --> Physics 
	```
will render this chart

```mermaid 
graph LR 
A{Biology} --> Chemistry
A -- nope --> Geology
Chemistry --> Physics 
```

---
## Sequence Diagram
This code 
	```mermaid 
	sequenceDiagram 
	Alice->>+John: Hello John, how are you? 
	Alice->>+John: John, can you hear me? 
	John-->>-Alice: Hi Alice, I can hear you! 
	John-->>-Alice: I feel great! 
	```
Will render this chart
```mermaid 
sequenceDiagram 
Alice->>+John: Hello John, how are you? 
Alice->>+John: John, can you hear me? 
John-->>-Alice: Hi Alice, I can hear you! 
John-->>-Alice: I feel great! 
```
--- 

## Latex Math
This code with double $
	\begin{vmatrix} 
	a & b\\ c & d \
	end{vmatrix}=ad-bc
Will generate:
$$ \begin{vmatrix} 
a & b\\ c & d 
\end{vmatrix}
=ad-bc $$
This is an inline math expression $e^{2i\pi} = 1$. It is used with a single $, exemples : $x = 3$ , $a^2 + b^2 = a^2 + ab + b^2$
$$\int_{a}^b\int_{c}^d f(x,y)dxdy$$


---
# State Diagrams



```mermaid 
stateDiagram
    [*] --> Still
    Still --> [*]

    Still --> Moving
    Moving --> Still
    Moving --> Crash
    Crash --> [*]
```





---
# Pie Charts

```mermaid
pie title What Voldemort doesn't have?
         "FRIENDS" : 2
         "FAMILY" : 3
         "NOSE" : 45
```



---
# Callouts

     > [!note] title
     > text in callout
  

> **📝 note**
>



> **☑️ info todo**
>



> **📋 abstract summary tldr**
>



> **⚠️ tip hint important**
>



> **✅ success check done**
>



> **❓ question help faq**
>
> test





> **⚠️ warning caution attention**
>



> **❌ failure fail missing**
>
> attention, au passage du train...



> **⚡ danger error**
>



> **🐛 bug**
>



> **📝 example**
>



> **💬 quote cite**
>




> **❓ Can callouts be nested? **
>
> > [!todo] Yes!, they can. 
> > > [!example] You can even use multiple layers of nesting



## [All Obsidian Callouts](https://notes.nicolevanderhoeven.com/Obsidian+Callouts)



## Exemple of a code exemple in R


> **📌 Syntaxe mise en lumière pour R**
>
> Exemple de code trouvé sur internet :
>
>
> ```R
> help(*)
>
> > x <- 1 
> > mode(x) [1] 

"numeric" 
> > length(x) 
[1] 1 
> > A <- "Gomphotherium"; compar <- TRUE; z <- 1i 
> > mode(A); mode(compar); mode(z) [1] 
"character" [1] 
"logical" [1] 
"complex"
>
>```

---
# Gantt Diagrams
```mermaid
gantt 
	title A Gantt Diagram 
	dateFormat DD/MM 
		section Prise d'informations
			Comparaison technique : done, ct, 15/02, 30d
		section Infrastructure 
			Setting up SQL Server :done, sql, after ct, 30d 
			Setting up Power Platform :done, ppf, 01/04, 20d 
		section ETL
			Gathering Data from FSE : after sql, 20d 
```

