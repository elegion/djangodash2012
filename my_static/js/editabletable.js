/*
 Table editable by clicking on cell (needs hidden form in html)
 ex. <form method="post">
 <input type="hidden" name="teststep" value="1">
 <input type="hidden" name="action" value="save_step">
 <table class="params js_params table table-striped table-bordered">
 <tbody>

 <tr class="step_count">
 <td><input type="hidden" name="count" value="{random:1:d}">count</td>
 <td>{random:1:d}</td>
 </tr>

 <tr class="step_trim_user">
 <td><input type="hidden" name="trim_user" value="true">trim_user</td>
 <td>true</td>
 </tr>

 <tr class="step_screen_name">
 <td><input type="hidden" name="screen_name" value="alarin_ru">screen_name</td>
 <td>alarin_ru</td>
 </tr>

 </tbody>
 </table>
 </form>
 */
EditableTable = {};
EditableTable.init = function($table, changedCallback) {
    EditableTable._$table = $table;
    EditableTable._changedCallback = changedCallback;
    if($table.length == 0) {
        return;
    }
    $table.find('td').click(EditableTable.cellClick);

    $table.find('tr').hover(EditableTable.showDelete, EditableTable.hideDelete);
}
EditableTable.cellClick = function() {
    var $this = $(this);
    if ($this.find('input.inplace').length == 0) {
        EditableTable.hideAllDelete();
        EditableTable.hideAllInputs();

        var $input = $('<input type="text" class="inplace">');
        $input.val($this.text());
        $input.keyup(EditableTable.inputChanged);
        $input.change(EditableTable.inputChanged);

        $this.empty();
        $this.append($input);
    }
}
EditableTable.inputChanged = function() {
    if (EditableTable._changedCallback) {
        EditableTable._changedCallback(this);
    }
    var $this = $(this);
    var $input = $this.parent().parent().find('input[type="hidden"]');
    if($this.parent().hasClass('name')) {
        $input.attr('name', 'js_' + $this.val());
    }
    if($this.parent().hasClass('value')) {
        $input.attr('value', $this.val());
    }
}

EditableTable.hideInput = function() {
    var $this = $(this);
    $this.parent().text($this.val());
    $this.change();
    $this.remove();
}

EditableTable.hideAllInputs = function() {
    EditableTable._$table.find('input.inplace').each(EditableTable.hideInput);
}

EditableTable.showDelete = function() {
    var $this = $(this);
    if ($this.find('.delete-button').length != 0) {
        $this.find('.delete-button').show();
    } else {
        var $delbtn = $('<i class="delete-button">&times;</i>');
        $delbtn.click(function(){
            EditableTable._changedCallback($this);
            $this.remove();
        });
        $this.find('td').first().prepend($delbtn);
    }
}

EditableTable.hideDelete = function () {
    $(this).find('.delete-button').remove();
}

EditableTable.hideAllDelete = function() {
    EditableTable._$table.find('.delete-button').remove();
}
