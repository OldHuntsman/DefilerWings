# coding=utf-8
#__author__ = 'Hikke_kun'

init -10 python:
    # По-умолчанию не генерируем документацию.
    # Для генерации можно добавить в options_local.rpy(не включен в репозиторий) в более поздний init блок, например:
    #init -2 python:
    #    gendoc = True
    gendoc = False

init -1 python:
    if 'codecs' not in globals():
        import codecs
    if 'sys' not in globals():
        import sys
    if 'inspect' not in globals():
        import inspect
    sys.setdefaultencoding("UTF-8")
    class Test:
        """ Олололо
        Test docstring
        """
        pass

        def othermethod(self):
            """
            othermethod docstring
            """

        @staticmethod
        def staticmethodtest():
            """
            staticmethod docstring
            """

        def somemethod(self, param="smth"):
            """
            :param param: Some parameter
            Method docstring
            """
            pass

    class Pygendoc:
        doc_classes = []

        def __init__(self):
            pass

        def generate(self):
            import renpy.store as store
            import os
            doc_dir = os.path.abspath(os.path.join(config.basedir, "source/inc"))
            gen = (store.__getattribute__(i) for i in dir(store) if i in self.doc_classes)
            gen = (store.__getattribute__(i) for i in self.doc_classes)
            for doc_class in gen:
                f = codecs.open(os.path.join(doc_dir, doc_class.__name__+".rst"), "w", "utf-8")
                f.write('.. py:class:: `%s`\n\n' % doc_class.__name__)
                # Пишем документацию для класса
                if doc_class.__doc__ is not None:
                    f.write(codecs.decode(inspect.getdoc(doc_class), 'utf-8'))
                    f.write('\n\n')
                f.write("Methods\n")
                f.write("=======\n\n")
                for methodname, method in inspect.getmembers(doc_class, predicate=inspect.ismethod):
                    self.doc_classmethod(f, doc_class, method)
                f.write("Static methods\n")
                f.write("=========\n\n")
                for methodname, method in inspect.getmembers(doc_class, predicate=inspect.isfunction):
                    self.doc_staticmethod(f, doc_class, method)
                f.close()
            return

        def doc_classmethod(self, file, doc_class, method):
            if file is None or doc_class is None or method is None:
                return
            if method.__doc__ is not None:
                # Заголовок для метода
                file.write('.. py:classmethod:: `%s %s`\n\n' % (method.__name__, inspect.getargspec(method)))
                # Содержание докстринга
                for line in inspect.getdoc(method).split('\n'):
                    file.write('   %s\n' % codecs.decode(line, 'utf-8'))
                # Конец метода
                file.write('\n\n')

        def doc_staticmethod(self, file, doc_class, method):
            if file is None or doc_class is None or method is None:
                return
            if method.__doc__ is not None:
                # Заголовок для метода
                file.write('.. py:staticmethod:: `%s`\n\n' % method.__name__)
                # Содержание докстринга
                for line in inspect.getdoc(method).split('\n'):
                    file.write('   %s\n' % codecs.decode(line, 'utf-8'))
                file.write('\n\n')

    if 'gendoc' in globals() and gendoc:
        pygendoc = Pygendoc()

init 100 python:
    if 'gendoc' in globals() and gendoc:
        pygendoc.doc_classes.append('Test')
        if 'Thief' not in globals():
            from pythoncode.characters import Thief
        pygendoc.doc_classes.append('Thief')
        pygendoc.generate()

label gendoc:
    python hide:
        ######################
        # Configuration values
        ######################

        # the list of keywords that can follow an :odoc: tag
        keywords = ["logger"]
        # this file header should be added to each file at the top.
        fileHeader = ".. Automatically generated file - do not modify."
        # this should be changed to point to a dir called inc in your sphinx source dir
        incPath = _config.gamedir + "/../sphinx/source/inc/"

        ######################
        # Extraction of doc
        ######################

        import inspect
        import re
        docLog = Logger("docLog.log")
        g = {}
        g.update(globals())


        addToDoc = []

        # Parse for docstrings by seacrching methods and classes defined in globals
        # if a class has methods with docstrings, we'll pull those in as well by using getattr()
        for key in g:
            if (g[key].__doc__) != None:
                for line in (g[key].__doc__).split("\n"):
                    if ":root:" in line:
                        if (line.strip())[6:] in keywords:
                            addToDoc.append(g[key].__doc__)
                            if inspect.isclass(g[key]):
                                for method in dir(g[key]):
                                    myMethod = getattr(g[key], method)
                                    if(myMethod.__doc__) != None:
                                         for mLine in (myMethod.__doc__).split("\n"):
                                            if ":root:" in mLine:
                                                if (mLine.strip())[6:] in keywords:
                                                    addToDoc.append(myMethod.__doc__)

        # Removes duplicates
        addToDoc = list(set(addToDoc))

        # Now we'll work on parsing out info from the docstring and sending it to the inc dir as a file

        for item in d_addToDoc:
            doc=""
            name=""
            itemType=""
            docString=""
            first = True
            indent = 0

            # First find what doc to use
            lineList = reduce(lambda acc, elem: acc[:-1] + [acc[-1] + elem] if elem == "\n" else acc + [elem], re.split("(%s)" % re.escape("\n"), item), [])
            for line in lineList:
                if ":root:" in line:
                    doc = line.strip()[5:]
                if ":type:" in line:
                    itemType = line.strip()[6:]
                if ":name:" in line:
                    name = line.strip()[6:]

            # Now try get other lines and add them to the docString

                if ":root:" not in line:
                    if ":type:" not in line:
                        if ":name:" not in line:
                            if first and  not line.isspace():
                                indent = len(line) - len(line.lstrip())
                                first = False

                            docString += line[indent:]

            if itemType == "class" or type == "function":
                docFile = open(incPath + doc, "w")
            elif itemType == "method":
                docFile = open(incPath + doc + "." + name, "w")
            else:
                postError("Item type is not a class, function, or method!\n itemType: " + itemType)
            docFile.write(fileHeader + "\n" + docString)
            docFile.close()
