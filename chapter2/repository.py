import abc
import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, batch: model.Batch):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        raise NotImplementedError

class FakeRepository(AbstractRepository):
    def __init__( self, batches):
        self._batches = set( batches)

    def add( self, batch):
        self._batches.add( batch)

    def get( self, reference):
        return next( b for b in self._batches if b.reference == reference)

    def list( self):
        return list( self._batches)



class SqlRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, batch):
        # self.session.execute('INSERT INTO ??
        ...

    def get(self, reference) -> model.Batch:
        # self.session.execute('SELECT ??
        ...
