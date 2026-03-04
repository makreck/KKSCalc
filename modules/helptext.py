
general_usage = '''
<p><h2>General usage:</h2>
<ul style="list-style-type: square;">
<li>Type your formula like <b>1+1</b> and press enter key. Do not add a <b>=</b>.</li>
<li>Use <b>#</b> prefix to mark special values, such as date/time strings or roman numbers.<br>
Example for date string: <b>#2026-02-24</b>. After pressing enter, the date is converted into a date-factor which can be used for difference calculations.<br>
Example for roman number use: <b>#MMXXVI</b>. After pressing enter it is converted into 2026.<br>
<li>You can use <b>.rom</b> command for converting a decimal number into a roman number.</li>
<li>With the <b>#</b> sign, you can use the result directly in calculations.<br>
Example: <b>#2026-02-01-#VI</b> -> 162145.0-6.0 -> 162139.0.</li>
<li>Use the <b>0x</b> prefix to type hexadecimal numbers. Example: <b>0xff</b> for 255 decimal.</li>
<li>Use the <b>0b</b> prefix to type binary numbers. Example: <b>0b10101010</b> for 170 decimal.</li>
<li>The result value is automatically converted to the set output format (see toolbar).</li>
</ul></p><br>

<p><h2>Variables:</h2>
<ul style="list-style-type: square;">
<li>If you want to store a result in a variable, you can assign it using a <b>=</b>. Do not use the <b>=</b> for starting the calculation.</li>
<li>Example for assigning a value to a variable: <b>a=5+1</b>. After pressing enter, the result <b>6</b> is assigned to the variable <b>a</b>.</li>
<li>You can use indexed variables like <b>a[3]</b>. This allows to store a value in a variable where the index is calculated.<br>
Example: <b>x=1+2</b> enter, <b>a[x+1]=99</b> enter. The result is that the value <b>99</b> is assigned to the variable <b>a[4]</b>.</li>
<li>Nested index variables are possible. Each index is represented by a sub-formula.<br>
Example: <b>x[0]=1</b> enter <b>x[1]=2</b> enter <b>x[x[0]]</b> enter results in <b>2.0</b>.
</ul></p>

<p><h2>Clipboard support:</h2>
<ul style="list-style-type: square;">
<li>You can copy and past in editor as common doing.</li>
<li>You can use the copy menu to copy the latest result into the clipboard.</li>
<li>You can use the .paste command to parse clipboard content into variables. Space separated numbers are assigned as array of the variable name.
You can copy a line in LibreOffice Calc and paste all columns into a variable array.<br>
<b>Note: Comma Separated Values (CSV-format) is not directly accepted because comma can be used a decimal digit separator or decimal point.</b></li>
</ul></p>

<p><h2>Macros:</h2>
<ul style="list-style-type: square;">
<li>A macro consists of a name and a list of commands and/or operations.</li>
<li>Any macro is identified by its name. Any macro name must be unique.</li>
<li>When a macro is called, the calculator executes each line of text exactly as if it had just been entered.</li>
<li>You can access a macro by selecting it from the menu or, for the first 12 macros, by pressing the corresponding function key F1 to F12.</li>
<li>To delete an existing macro, open the macro editor and remove the name. Then close the editor. The macro with the previous name will then be deleted.</li>
</ul></p>
'''
