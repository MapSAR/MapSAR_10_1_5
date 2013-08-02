set args=WScript.Arguments
wscript.quit MsgBox(Replace(Replace(args.item(1),"{cr}",vbNewLine,1,-1,1),"{qt}",Chr(34),1,-1,1),args.item(2),args.item(0))