/*
 Editable table, needs special layout with hidden forms
 */
EditableTable = {};

EditableTable.init = function($table, changedCallback) {
    EditableTable._$table = $table;
    EditableTable._changedCallback = changedCallback;

//    EditableTable.editMode(true);
//    if($table.length == 0) {
//        return;
//    }
//    $table.find('td').click(EditableTable.cellClick);
//
//    $table.find('tr').hover(EditableTable.showDelete, EditableTable.hideDelete);
//    $table.hover(EditableTable.mouseover, EditableTable.mouseout);
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
    $this.parent().find('span').text($this.val());
    $this.change();
    $this.remove();
}

EditableTable.hideAllInputs = function() {
    EditableTable._$table.find('input.inplace').each(EditableTable.hideInput);
}

EditableTable.hideDelete = function () {
    $(this).find('.delete-button').remove();
}

EditableTable.hideAllDelete = function() {
    EditableTable._$table.find('.delete-button').remove();
}

EditableTable.showAddButton = function() {
    var $this = EditableTable._$table;
    if ($this.next('.add-button').length != 0) {
        $this.next('.add-button').show();
    } else {
        var $addbtn = $('<a class="btn add-button btn-addtestcase btn-success btn-mini"><i class="icon-plus icon-white"></i></a>');
        $addbtn.click(function(){
            var $newtr = $this.find('.row_template').first().clone();
            $newtr.removeClass('row_template');
            $newtr.show();
            $newtr.find('input.inplace').keyup(EditableTable.inputChanged);
            $newtr.find('input.inplace').change(EditableTable.inputChanged);
            EditableTable.addDeleteButton($newtr);
            $this.find('tr').first().before($newtr);
            return false;
        });
        $this.find('table').first().before($addbtn);
    }
}

EditableTable.addDeleteButton = function($row) {
//    var $row
//    if ($this.find('.delete-button').length != 0) {
//        $this.find('.delete-button').show();
//    } else {
        var $delbtn = $('<td><i class="delete-button btn-deletetestcase">&times;</i></td>');
        $delbtn.click(function(){
            $row.remove();
        });
        $row.prepend($delbtn);
//    }
}

EditableTable.mouseout = function() {
    var $this = $(this);
    $this.next('.add-button').hide();
}

EditableTable.editMode = function(table, on) {
    var $this = table;
    EditableTable._$table = table;
    if(on) {
        $this.find('td').each(function() {
            var $this = $(this);
            var $input = $('<input type="text" class="inplace">');
            $input.val($this.find('span').text());
            $input.keyup(EditableTable.inputChanged);
            $input.change(EditableTable.inputChanged);

            $this.find('span').empty();
            $this.append($input);
        });
        $this.find('tr').not('.row_template').each(function() {
           EditableTable.addDeleteButton($(this));
        });
        EditableTable.showAddButton();

        $this.find('.form-action').show();
    }
}