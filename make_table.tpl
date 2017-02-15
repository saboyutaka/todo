% rebase('base.tpl', title='Page Title')
<div class="row">
  <div class="col s12">
    <a href="/new" class="waves-effect waves-light btn right new-button">
      <i class="material-icons right">note_add</i>
      New Todo
    </a>
  </div>
</div>
<div class="row tasks">
  %for row in rows:
    <div class="col s12 m4">
      <a href="/show/{{row[0]}}">
        <div class="task card-panel grey lighten-5 hoverable">
          <span class="truncate content">
            {{row[1]}}
          </span>
        </div>
      </a>
    </div>
  %end
</div>
