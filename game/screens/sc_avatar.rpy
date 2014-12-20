# coding=utf-8
screen sc_avatar:
    if game.currentCharacter is not None:               # Если определен тот кто говорит в данный момент
        if game.currentCharacter.avatar is not None:    # И у него есть аватарка
            add game.currentCharacter.avatar            # Показываем аватарку
            add "img/bg/frame.png"                      # И рамочку вокруг
