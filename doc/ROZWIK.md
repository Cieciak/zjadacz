# Rozwik Language Specification
## Buildin
### String
> "raw text"
### Regular Expression
> /regex body/

## Selectors
### Choice
> [p1 p2 p3 ... pn]
### Sequence
> (p1 p2 p3 .. pn)

## Modifiers
### Many
> p*
### Many strict
> p+
### Optional
> p?

## Directives
### Use
> #use file.py