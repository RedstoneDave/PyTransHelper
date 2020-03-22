# PyTransHelper
 a Python Translation Helper

## version
 0.1.3

## Usage
 Any kind of Translation
 Used for translating Wikitext by the user himself

## How to use
 This chapter tells the way to use this software
### Buttons
 At the bottom of the UI, there are several buttons,
 each of them has a different function.
 **Unless otherwise stated, "Saving the translation" means saving it in the cache, which means you need to *Save* often.**
#### Load
 This button is used for loading the translation files(**text.in** for source file, **text.out** for result file by default, defined in **settings.json**) you last worked on, and initalize important variables.
#### Init
 This button is used for initialize the source from the *Source* box, and generate the translation files, where **text.out** has only line breaks(a.k.a. '\n'). and also initalize important variables.
#### SkipFd
 When you press this button, you are skipping to the previous line of the translation **without saving the present translation**, not available when translating the first line. 
#### Prev
 When you press this button, you are **saving the present translation result** and going to the previous line of the translation, not available when translating the first line.
#### Next
 When you press this button, you are **saving the translation result** and going to the next line of the translation.
#### SkipBd
 When you press this button, you are skipping to the next line of the translation **without saving the present translation**. 
#### AutoTrans
 Using Google translation to translate the text in the *Source* box, and append the result to the end of *Result* box.
#### Copy
 Clear the *Result* box and copy the text in the *Source* box to the *Result* box.
#### Save
 **DO THIS OFTEN!** This saves your translation result **to the translation files**.
#### Jump
 When you press this button, you could jump to a specified line after **saving the present result**.
#### Exce
 This button is used to excecute the code in *Result* box, used for debugging.
### Hot Keys
 Some hot keys are defined in settings.json. At present, each hot key is related to a button.
#### Ctrl-i
 The same as *Init* button
#### Alt-left / Alt-right
 The same as *SkipFd* / *SkipBd* button
#### Ctrl-left / Ctrl-right
 The same as *Prev* / *Next* button
#### Alt-c
 The same as *Copy* button
#### Ctrl-s
 The same as *Save* button
#### Ctrl-j
 The same as *Jump* button