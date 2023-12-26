#Requires AutoHotkey v2.0

CoordMode("Mouse", "Screen")

full_command_line := DllCall("GetCommandLine", "str")

if not (A_IsAdmin or RegExMatch(full_command_line, " /restart(?!\S)"))
{
    try
    {
        if A_IsCompiled
            Run '*RunAs "' A_ScriptFullPath '" /restart'
        else
            Run '*RunAs "' A_AhkPath '" /restart "' A_ScriptFullPath '"'
    }
    ExitApp
}


click1_X := 0
click1_Y := 0

click2_X := 0
click2_Y := 0

; script starts from here
SetTitleMatchMode(2)

; Number of times you want to run this experiment
replicate := 1

; Time delay in milliseconds
test_time := 1000 ; ensure this is longer than estimated time for test

; The title or part of the title of the window to activate
labview_window := String("Chrome_WidgetWin_1")

; The title or part of the title of the window to close
pop_up_window := String("Notepad")

; Coordinates of the buttons to click

; Ask user to set coordinates for each button
MsgBox("position your mouse over the first button and press enter")
MouseGetPos(&click1_X, &click1_y)

MsgBox("position your mouse over the first button and press enter")
MouseGetPos(&click2_X, &click2_Y)

Loop(replicate) {
    Sleep(test_time)

    ; Close pop-up excel file
    If WinExist("ahk_class" . pop_up_window) { 
        WinClose
     }


    ; ensure labview in focus
    If WinExist("ahk_class" . labview_window) {

        WinActivate

        Sleep(1000) ; Wait for a bit to ensure the window is active

        ; Click the first button
        Click(click1_X, click1_Y)
        Sleep(2000) ; Wait for 500 milliseconds

        ; Click the third button
        Click(click2_X, click2_Y)
        Sleep(2000) ; Wait for 500 milliseconds
        
    } else {
        MsgBox("no labview found")
    }
}

; end of script

