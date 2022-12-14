/* Copyright 2010-2018 Jesse McGrew
 * 
 * This file is part of ZILF.
 * 
 * ZILF is free software: you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 * 
 * ZILF is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with ZILF.  If not, see <http://www.gnu.org/licenses/>.
 */

using JetBrains.Annotations;
using Zilf.Diagnostics;
using Zilf.Interpreter;
using Zilf.Interpreter.Values;
using Zilf.Interpreter.Values.Tied;
using Zilf.Language;

namespace Zilf.ZModel.Values
{
    [BuiltinType(StdAtom.CONSTANT, PrimType.LIST)]
    class ZilConstant : ZilTiedListBase
    {
        public ZilConstant([NotNull] ZilAtom name, [NotNull] ZilObject value)
        {
            Name = name;
            Value = value;
        }

        /// <exception cref="InterpreterError"><paramref name="list"/> has the wrong number or types of elements.</exception>
        [NotNull]
        [ChtypeMethod]
        public static ZilConstant FromList([NotNull] ZilListBase list)
        {
            if (!list.HasLength(2))
                throw new InterpreterError(InterpreterMessages._0_Must_Have_1_Element1s, "list coerced to CONSTANT", 2);

            if (!list.Matches(out ZilAtom nameAtom, out ZilObject value))
                throw new InterpreterError(InterpreterMessages.Element_0_Of_1_Must_Be_2, 1, "list coerced to CONSTANT", "an atom");

            return new ZilConstant(nameAtom, value);
        }

        [NotNull]
        public ZilAtom Name { get; }

        [NotNull]
        public ZilObject Value { get; }

        protected override TiedLayout GetLayout()
        {
            return TiedLayout.Create<ZilConstant>(
                x => x.Name,
                x => x.Value);
        }

        public override StdAtom StdTypeAtom => StdAtom.CONSTANT;
    }
}