"""figure.py - Mini-figure construction classes for the ldraw Python package.

Copyright (C) 2008 David Boddie <david@boddie.org.uk>

This file is part of the ldraw Python package.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# pylint: disable=missing-docstring
from ldraw.geometry import Identity, Matrix, Vector, XAxis, YAxis, ZAxis
from ldraw.pieces import Piece


def dependent_piece(dep):
    """Mark a piece method as dependent on another piece existing."""

    def decorator(fn):
        def wrapped(self, *args, **kwargs):
            try:
                dependent_object = self.pieces_info[dep]
                return fn(self, dependent_object, *args, **kwargs)
            except KeyError:
                return None

        return wrapped

    return decorator


# hardcoded
Airtanks = "3838"
HipsAndLegs = "3815c01"
Hips = "3815b"
ArmLeft = "3819"
ArmRight = "3818"
Hand = "3820"
LegLeft = "3817b"
LegRight = "3816b"
Torso = "973"
Head = HeadWithSwSmirkAndBrownEyebrowsPattern = "3626bps5"


class Person:
    """Representation of a LEGO minifigure."""

    def __init__(
        self,
        position: Vector | None = None,
        matrix: Matrix | None = None,
        group=None,
    ):
        self.position = position if position is not None else Vector(0, 0, 0)
        self.matrix = matrix if matrix is not None else Identity()
        self.pieces_info = {}
        self.group = group

    def head(self, colour, angle=0, part=Head):
        """Displacement from torso."""
        displacement = self.matrix * Vector(0, -24, 0)
        piece = Piece(
            colour,
            self.position + displacement,
            self.matrix * Identity().rotate(angle, YAxis),
            part,
            self.group,
        )
        self.pieces_info["head"] = piece
        return piece

    @dependent_piece("head")
    def hat(self, head, colour, part="3901"):
        """Add a hat piece to the figure's head."""
        # Displacement from head
        displacement = head.position + head.matrix * Vector(0, 0, 0)
        return Piece(colour, displacement, head.matrix, part, self.group)

    def torso(self, colour, part=Torso):
        """Torso piece."""
        return Piece(colour, self.position, self.matrix, part, self.group)

    def backpack(self, colour, displacement: Vector | None = None, part=Airtanks):
        """Displacement from torso."""
        _displacement = self.matrix * (
            displacement if displacement is not None else Vector(0, 0, 0)
        )
        return Piece(
            colour,
            self.position + _displacement,
            self.matrix,
            part,
            self.group,
        )

    def hips_and_legs(self, colour, part=HipsAndLegs):
        """Displacement from torso."""
        displacement = self.matrix * Vector(0, 32, 0)
        return Piece(
            colour,
            self.position + displacement,
            self.matrix,
            part,
            self.group,
        )

    def hips(self, colour, part=Hips):
        """Displacement from torso."""
        displacement = self.matrix * Vector(0, 32, 0)
        return Piece(
            colour,
            self.position + displacement,
            self.matrix,
            part,
            self.group,
        )

    def left_arm(self, colour, angle=0, part=ArmLeft):
        """Displacement from torso."""
        displacement = self.matrix * Vector(15, 8, 0)
        piece = Piece(
            colour,
            self.position + displacement,
            self.matrix
            * Identity().rotate(-10, ZAxis)
            * Identity().rotate(angle, XAxis),
            part,
            self.group,
        )
        self.pieces_info["left arm"] = piece
        return piece

    @dependent_piece("left arm")
    def left_hand(self, left_arm, colour, angle=0, part=Hand):
        """Add a left hand piece to the figure's left arm."""
        # Displacement from left hand
        displacement = left_arm.position + left_arm.matrix * Vector(4, 17, -9)
        matrix = (
            left_arm.matrix
            * Identity().rotate(40, XAxis)
            * Identity().rotate(angle, ZAxis)
        )
        piece = Piece(colour, displacement, matrix, part, self.group)
        self.pieces_info["left hand"] = piece
        return piece

    @dependent_piece("left hand")
    def left_hand_item(self, left_hand, colour, displacement, angle=0, part=None):
        """Displacement from left hand."""
        if not part:
            return None
        # Displacement from left hand
        displacement = left_hand.position + left_hand.matrix * displacement
        matrix = (
            left_hand.matrix
            * Identity().rotate(10, XAxis)
            * Identity().rotate(angle, YAxis)
        )
        return Piece(colour, displacement, matrix, part, self.group)

    def right_arm(self, colour, angle=0, part=ArmRight):
        """Displacement from torso."""
        displacement = self.matrix * Vector(-15, 8, 0)
        piece = Piece(
            colour,
            self.position + displacement,
            self.matrix
            * Identity().rotate(10, ZAxis)
            * Identity().rotate(angle, XAxis),
            part,
            self.group,
        )
        self.pieces_info["right arm"] = piece
        return piece

    @dependent_piece("right arm")
    def right_hand(self, right_arm, colour, angle=0, part=Hand):
        """Add a right hand piece to the figure's right arm."""
        # Displacement from right arm
        displacement = right_arm.position + right_arm.matrix * Vector(-4, 17, -9)
        matrix = (
            right_arm.matrix
            * Identity().rotate(40, XAxis)
            * Identity().rotate(angle, ZAxis)
        )
        piece = Piece(colour, displacement, matrix, part, self.group)
        self.pieces_info["right hand"] = piece
        return piece

    @dependent_piece("right hand")
    def right_hand_item(self, right_hand, colour, displacement, angle=0, part=None):
        """Add a right hand item."""
        if not part:
            return None
        # Displacement from right hand
        displacement = right_hand.position + right_hand.matrix * displacement
        matrix = (
            right_hand.matrix
            * Identity().rotate(10, XAxis)
            * Identity().rotate(angle, YAxis)
        )
        return Piece(colour, displacement, matrix, part, self.group)

    def left_leg(self, colour, angle=0, part=LegLeft):
        """Add a left leg."""
        displacement = self.matrix * Vector(0, 44, 0)
        piece = Piece(
            colour,
            self.position + displacement,
            self.matrix * Identity().rotate(angle, XAxis),
            part,
            self.group,
        )
        self.pieces_info["left leg"] = piece
        return piece

    @dependent_piece("left leg")
    def left_shoe(self, left_leg, colour, angle=0, part=None):
        """Add a shoe on the left."""
        if not part:
            return None
        # Displacement from left leg
        displacement = left_leg.position + left_leg.matrix * Vector(10, 28, 0)
        matrix = left_leg.matrix * Identity().rotate(angle, YAxis)
        return Piece(colour, displacement, matrix, part, self.group)

    def right_leg(self, colour, angle=0, part=LegRight):
        """Add a right leg."""
        displacement = self.matrix * Vector(0, 44, 0)
        piece = Piece(
            colour,
            self.position + displacement,
            self.matrix * Identity().rotate(angle, XAxis),
            part,
            self.group,
        )
        self.pieces_info["right leg"] = piece
        return piece

    @dependent_piece("right leg")
    def right_shoe(self, right_leg, colour, angle=0, part=None):
        """Add a shoe on the right."""
        if not part:
            return None
        # Displacement from right leg
        displacement = right_leg.position + right_leg.matrix * Vector(-10, 28, 0)
        matrix = right_leg.matrix * Identity().rotate(angle, YAxis)
        return Piece(colour, displacement, matrix, part, self.group)
