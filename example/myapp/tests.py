from django.test import TestCase

from .models import Child, Parent

class SoftDeleteTestCase(TestCase):
    def test_reverse_relation(self):
        # Make sure there are no objects at the start.
        self.assertEqual(Parent.objects.count(), 0)
        self.assertEqual(Child.objects.count(), 0)

        # Create 1 parent.
        parent = Parent.objects.create(name='Parent')

        # Make sure the parent does not have a child.
        with self.assertRaises(Child.DoesNotExist):
            nothing = parent.child

        # Create 1 child.
        child = Child.objects.create(
            name='Child',
            parent=parent
        )

        # Make sure we have 1 of each.
        self.assertEqual(Parent.objects.count(), 1)
        self.assertEqual(Child.objects.count(), 1)

        # Make sure the relations work as expected.
        self.assertEqual(child.parent, parent)
        self.assertEqual(parent.child, child)

        # Make sure the `deleted_at` for child is not set.
        self.assertIsNone(parent.child.deleted_at)

        # Delete the child.
        child.delete()

        # Make sure there is not 1 parent and 0 children.
        self.assertEqual(Parent.objects.count(), 1)
        self.assertEqual(Child.objects.count(), 0)

        # Make sure the `deleted_at` for child is set.
        self.assertIsNotNone(parent.child.deleted_at)

        # Make sure the parent does not have a child, as it is now deleted.
        # Getting the parent from the database, to make sure the problem is not
        # caused by some cached data. This test fails.
        with self.assertRaises(Child.DoesNotExist):
            nothing = Parent.objects.first().child
