
general_usage = '''
<p><h2>General usage:</h2>
<ul style="list-style-type: square;">
<li>Type your formula like <b>1+1</b> and press return key. Do not add a <b>=</b>.</li>
<li>Use <b>#</b> prefix to mark special values, such as date/time strings or roman numbers.<br>
Example for date string: <b>#2026-02-24</b>. After pressing return, the date is converted into a date-factor which can be used for difference calculations.<br>
Example for roman number use: <b>#MMXXVI</b>. After pressing return it is converted into 2026.<br>
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
<li>Example for assigning a value to a variable: <b>a=5+1</b>. After pressing return, the result <b>6</b> is assigned to the variable <b>a</b>.</li>
<li>You can use indexed variables like <b>a[3]</b>. This allows to store a value in a variable where the index is calculated.<br>
Example: <b>x=1+2</b> return, <b>a[x+1]=99</b> return. The result is that the value <b>99</b> is assigned to the variable <b>a[4]</b>.</li>
</ul></p>
'''
