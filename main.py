from intersection import Intersection


def main():
    inter = Intersection(2, 2)
    print("Vehicle 1, lane 1, speed 2, distance 0:",
          inter.get_reservation(1, 1, None, 2, 0))
    print("Vehicle 2, lane 1, speed 2, distance 8:",
          inter.get_reservation(2, 1, None, 1, 2))
    print("Vehicle 3, lane 4, speed 2, distance 9:",
          inter.get_reservation(3, 4, None, 2, 8))
    print("Vehicle 3, lane 4, speed 1, distance 9:",
          inter.get_reservation(3, 4, None, 1, 8))


if __name__ == '__main__':
    main()
