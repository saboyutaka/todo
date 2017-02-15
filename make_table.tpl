%#template to generate a HTML table from a list of tuples (or list of lists, or tuple of tuples or ...)
% rebase('base.tpl', title='Page Title')
<p>The ssssopen items are as follows:</p>
<a href="/new">New Todo</a>
<table border="1">
%for row in rows:
  <tr>
  %print(row)
  %for col in row:
    <td>{{col}}</td>
  %end
  <td>
    <a href="/show/{{row[0]}}">Show</a>
  </td>
  </tr>
%end
</table>
